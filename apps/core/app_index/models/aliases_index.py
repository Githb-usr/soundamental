# ==========================================
# 🔤 Variations / Alias d'entrées (fichier dédié)
# ==========================================
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from unidecode import unidecode
import re

# Import des modèles locaux nécessaires
from .base_models import Category            # catégorie (copie pour cohérence/indexation)
from .index_entry import IndexEntry          # entrée principale utilisée comme "source de vérité"


class IndexAlias(models.Model):
    """
    Variation orthographique d'une entrée d'index (alias, translittération, aka, faute courante, etc.).
    - L'alias est relié à une entrée principale (IndexEntry).
    - La catégorie est recopiée depuis l'entrée principale (cohérence).
    - Une version "normalisée" est stockée pour l'unicité et la recherche rapide.
    - À l'affichage, l'alias apparaît comme une ligne normale (même catégorie) et renvoie
      vers les mêmes liens/URL que l'entrée principale.
    """
    entry = models.ForeignKey(
        IndexEntry,
        on_delete=models.CASCADE,
        related_name="aliases",  # permet: entry.aliases.all()
        verbose_name="Entrée principale"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        editable=False,  # maintenu automatiquement depuis entry.category
        verbose_name="Catégorie (copie)"
    )
    alias = models.CharField(
        max_length=255,
        verbose_name="Alias",
        help_text="Variation du nom (ex. : '2Unlimited', 'Mylene Farmer', 'Daft punk', 'Jackson, Michael')."
    )
    alias_normalized = models.CharField(
        max_length=255,
        editable=False,
        db_index=True,
        verbose_name="Alias normalisé",
        help_text="Généré automatiquement : sans accents/ponctuation, en minuscules, espaces compactés."
    )
    
    is_listed = models.BooleanField(
        default=True,
        verbose_name="Afficher dans l’index",
        help_text=(
            "Si décoché, l’alias reste pris en compte pour la recherche et pointe vers les "
            "mêmes liens que l’entrée principale, mais il n’est pas listé dans l’index."
        ),
    )


    class Meta:
        verbose_name = "Alias d'index"
        verbose_name_plural = "Index - Alias"
        # Un alias normalisé est unique au sein d'une catégorie (évite doublons inter-entrées)
        constraints = [
            models.UniqueConstraint(
                fields=["alias_normalized"],
                name="uniq_alias_normalized_global"
            )
        ]
        indexes = [
            models.Index(fields=["alias_normalized"]),
            models.Index(fields=["entry"]),
        ]
        ordering = ["alias"]

    def __str__(self):
        return f"{self.alias} → {self.entry.name}"

    # -------------------
    # Normalisation forte
    # -------------------
    @staticmethod
    def normalize(value: str) -> str:
        """
        Normalise pour comparaison/unicité :
        - translittération ASCII (supprime accents),
        - remplace tirets/underscores/slash/points par espaces,
        - supprime ponctuation courante (apostrophes droites/typographiques, (), [], {}, &,+,!,?,:;, etc.),
        - met en minuscules,
        - compresse les espaces multiples,
        - conserve les chiffres (utile pour 'MJ (2)').
        """
        if not value:
            return ""
        txt = value.replace("’", "'")  # homogénéise l’apostrophe typographique
        # remplace certains séparateurs par espaces
        txt = re.sub(r"[-_/\.]", " ", txt)
        # supprime ponctuation (mais garde chiffres et lettres)
        txt = re.sub(r"[\'\"`()\[\]{}&+!?:;~,^°•·|\\]", "", txt)
        # translittère et met en minuscules
        txt = unidecode(txt).lower()
        # compresse espaces
        txt = " ".join(txt.split())
        return txt

    # -----------
    # Cohérence
    # -----------
    def clean(self):
        """
        Vérifications applicatives :
        1) la catégorie copiée doit correspondre à celle de l'entrée,
        2) interdire qu'un alias = nom principal de sa propre entrée (normalisé),
        3) interdire qu'un alias (normalisé) = nom principal (normalisé) d'une autre entrée de la même catégorie.
        4) interdire qu'un alias (normalisé) = alias (normalisé) d'une autre entrée de la même catégorie.
        """
        super().clean()

        # 1) Catégorie cohérente avec l'entrée
        if self.entry and self.category_id and self.category_id != self.entry.category_id:
            self.category = self.entry.category  # forcé (pas d'erreur bloquante)

        # Prépare normalisés
        alias_norm = IndexAlias.normalize(self.alias or "")
        principal_norm = IndexAlias.normalize(self.entry.name if self.entry else "")

        # 2) Alias = nom principal (même entrée) → interdit (évite ligne doublon)
        if alias_norm and principal_norm and alias_norm == principal_norm:
            raise ValidationError({"alias": "Cet alias équivaut (normalisé) au nom principal de l'entrée."})

        # 3) Conflit avec un NOM PRINCIPAL d'une AUTRE entrée (toutes catégories)
        conflicts = IndexEntry.objects.exclude(pk=self.entry_id).only("id", "name")
        for e in conflicts:
            if IndexAlias.normalize(e.name) == alias_norm:
                raise ValidationError({"alias": (
                    f"Conflit avec l'entrée '{e.name}' (toute catégorie). "
                    f"Incrémentez le nom (ex. '... (2)') si intentionnel."
                )})

        # 4) Conflit avec un AUTRE ALIAS (toutes catégories)
        other_alias = (
            IndexAlias.objects
            .filter(alias_normalized=alias_norm)
            .exclude(pk=self.pk)
            .select_related("entry")
            .first()
        )
        if other_alias:
            raise ValidationError({"alias": (
                f"Alias déjà utilisé par l'entrée '{other_alias.entry.name}' (toute catégorie). "
                f"Modifiez l'alias ou incrémentez-le (ex. '... (2)')."
            )})

    def save(self, *args, **kwargs):
        # Alimente d'abord les champs dépendants
        if self.entry and (not self.category_id or self.category_id != self.entry.category_id):
            self.category = self.entry.category
        self.alias_normalized = IndexAlias.normalize(self.alias or "")

        # Vérification applicative globale avant écriture
        self.full_clean()

        super().save(*args, **kwargs)


# ==========================================================
# 💡 Génération d'alias suggérés (articles FR/EN + inversion)
# ==========================================================

def _suggest_article_aliases(name: str) -> list[str]:
    """
    Suggère les alias basés sur les articles en tête :
    - FR : Le, La, Les, L'/L’  → 'Forbans, Les' ; 'Affaire..., L’'
    - EN : The                → 'Beatles, The'
    Retourne 0..N suggestions (chaînes brutes, non normalisées).
    """
    if not name:
        return []

    # On respecte la casse d'origine de l'article de tête
    patterns = [
        (r"^\s*(Le)\s+(.+)$", "{rest}, {art}"),
        (r"^\s*(La)\s+(.+)$", "{rest}, {art}"),
        (r"^\s*(Les)\s+(.+)$", "{rest}, {art}"),
        (r"^\s*(L['’])\s*(.+)$", "{rest}, {art}"),
        (r"^\s*(The)\s+(.+)$", "{rest}, {art}"),
    ]
    out = []
    for pat, fmt in patterns:
        m = re.match(pat, name, flags=re.IGNORECASE)
        if m:
            art = m.group(1)       # article capturé (on garde sa forme/casse)
            rest = m.group(2).strip()
            # Cas L'/L’ : pas d’espace inutile
            suggestion = fmt.format(rest=rest, art=art)
            out.append(suggestion)
    return out


def _seems_personal_name_for_inversion(name: str) -> bool:
    """
    Heuristique prudente pour proposer inversion 'Nom, Prénom' (catégorie 'artiste' uniquement) :
    - exactement 2 mots séparés par espace,
    - chaque mot commence par majuscule suivie de minuscules (évite DJ/MC, sigles, etc.),
    - exclut quelques préfixes fréquents.
    """
    blocked_tokens = {"dj", "mc", "dr", "mr", "mrs", "ms", "sir", "saint", "st", "sainte"}
    parts = name.strip().replace("’", "'").split()
    if len(parts) != 2:
        return False

    def ok_word(w: str) -> bool:
        # Autorise lettres avec accents (on regarde la casse Python), refuse chiffres/punctuations évidentes
        return bool(re.match(r"^[A-ZÀ-Ý][a-zà-ÿ\-]+$", w))

    low = [p.lower() for p in parts]
    if any(p in blocked_tokens for p in low):
        return False
    return all(ok_word(p) for p in parts)


def _suggest_inversion_alias(name: str, category_code: str | None) -> list[str]:
    """
    Suggère 'Jackson, Michael' pour 'Michael Jackson' (catégorie 'artiste' uniquement),
    si l'heuristique _seems_personal_name_for_inversion() est satisfaite.
    """
    if not name or not category_code:
        return []
    if category_code.lower() != "artiste":
        return []
    if not _seems_personal_name_for_inversion(name):
        return []
    a, b = name.strip().replace("’", "'").split()
    return [f"{b}, {a}"]


def _filter_valid_candidates(entry: IndexEntry, candidates: list[str]) -> list[str]:
    """
    Filtre les suggestions pour éviter les conflits avant création (UNICITÉ GLOBALE) :
    - retire vides / égales (normalisées) au principal,
    - retire celles déjà existantes comme alias (toutes catégories),
    - retire celles qui égalent le nom principal d'une AUTRE entrée (toutes catégories).
    """
    principal_norm = IndexAlias.normalize(entry.name)
    seen = set()
    valid: list[str] = []

    # Tous alias normalisés (toutes catégories)
    existing_alias_norms = set(
        IndexAlias.objects.values_list("alias_normalized", flat=True)
    )

    # Tous autres noms principaux (normalisés), toutes catégories
    other_entries = IndexEntry.objects.exclude(pk=entry.pk).only("name")
    other_principal_norms = {IndexAlias.normalize(e.name) for e in other_entries}

    for cand in candidates:
        norm = IndexAlias.normalize(cand)
        if not norm:
            continue
        if norm == principal_norm:
            continue  # même que principal
        if norm in existing_alias_norms:
            continue  # déjà utilisé comme alias
        if norm in other_principal_norms:
            # conflit avec un autre nom principal → à toi d'incrémenter ("... (2)") si intentionnel
            continue
        if norm in seen:
            continue
        seen.add(norm)
        valid.append(cand)

    return valid

def suggest_aliases_for_entry(entry: IndexEntry) -> list[str]:
    """
    Génère la liste d'alias suggérés pour une entrée donnée (sans créer en BDD).
    Règles :
      - Articles FR/EN au début (Le/La/Les/L'/The) → alias avec article en fin.
      - Inversion Nom, Prénom (catégorie 'artiste' uniquement) si heuristique valide.
    """
    if not entry or not entry.name:
        return []
    suggestions = []
    suggestions += _suggest_article_aliases(entry.name)
    suggestions += _suggest_inversion_alias(entry.name, getattr(entry.category, "code", None))
    # Nettoyage / dédoublonnage final + anti-conflits
    return _filter_valid_candidates(entry, suggestions)


@receiver(post_save, sender=IndexEntry)
def auto_create_suggested_aliases(sender, instance: IndexEntry, created, **kwargs):
    """
    Ne crée les alias suggérés que lors de la CRÉATION d'une entrée.
    Évite les doublons quand l'admin enregistre une entrée + inlines (ordre: parent puis inlines).
    """
    if not created:
        return  # ← clé : on ne fait rien lors d'une modification

    try:
        candidates = suggest_aliases_for_entry(instance)
        for text in candidates:
            norm = IndexAlias.normalize(text)
            exists = IndexAlias.objects.filter(alias_normalized=norm).exists()
            if not exists:
                IndexAlias.objects.create(entry=instance, alias=text)
    except Exception:
        # Ne jamais casser la sauvegarde d'une entrée à cause des suggestions.
        pass
