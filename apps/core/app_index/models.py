from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from unidecode import unidecode

# ========================
# 📂 MODÈLES POUR L'INDEX
# ========================

class Category(models.Model):
    """
    Modèle représentant une catégorie pour les entrées de l'index.
    """
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code",
        help_text="Clé technique unique (ex: artiste, compilation, label, lexique, etc.)."
    )
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nom",
        help_text="Nom de la catégorie (ex: Artiste, Label, Compilation)."
    )
    label = models.CharField(
        max_length=100, 
        verbose_name="Libellé affiché (au pluriel, si besoin)"
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Description",
        help_text="Description de la catégorie."
    )

    def __str__(self):
        return self.label or self.name

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Index - Catégories"
        ordering = ["name"]

class PageType(models.Model):
    """
    Modèle représentant un type de page pour les entrées de l'index.
    """
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code technique",
        help_text="Identifiant technique, utilisé dans le code (ex: artiste_biography, label_history)."
    )
    label = models.CharField(
        max_length=100,
        verbose_name="Nom affiché",
        help_text="Nom affiché du type de page (ex: Biographie (Artistes))."
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Description",
        help_text="Description du type de page."
    )

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Type de page"
        verbose_name_plural = "Index - Types de pages"
        ordering = ["label"]


class IndexEntry(models.Model):
    """
    Modèle représentant une entrée de l'index général et thématique.
    - Une entrée correspond à un artiste, un label, une compilation, etc.
    - Les entrées sont générées dynamiquement, mais certaines infos (comme l'ID du forum) doivent être stockées.
    """
    name = models.CharField(
        max_length=255, unique=True, verbose_name="Nom",
        help_text="Nom officiel de l'entrée (ex: Michael Jackson, Top DJ Hits)"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Catégorie",
        help_text="Type d'entrée (artiste, compilation, label, etc.)"
    )
    id_forum = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="ID Forum",
        help_text="ID du forum sous la forme '12345-slug' (ex: 9699-stereotype)"
    )

    class Meta:
        indexes = [
            models.Index(fields=["category"]),  # Accélère les recherches par catégorie
            models.Index(fields=["name"]),  # Accélère les recherches par nom
        ]
        ordering = ["name"]  # Trie l’index par nom (A-Z)
        verbose_name = "Entrée de l'index"
        verbose_name_plural = "Index - Entrées"

    @cached_property
    def get_forum_url(self):
        """
        Génère et met en cache l'URL du forum pour cette entrée si un ID forum est renseigné.
        Exemple :
            id_forum = "12345-stereotype"
            ➝ Retourne : "https://www.soundamental.org/forum/topic/12345-stereotype"
        """
        return settings.LINK_BASES["forum"].format(self.id_forum) if self.id_forum else None

    @cached_property
    def get_links(self):
        base_urls = settings.LINK_BASES.get(self.category.code, {})
        template = settings.INDEX_LINK_TEMPLATES.get(self.category.code, [None] * 5)
        slugified_name = f"{self.id}-{unidecode(self.name).lower().replace(' ', '-')}"
        links = []
        for key in template[:-1]:  # on gère forum à part
            if not key:
                links.append(None)
                continue
            exists = PageExistence.objects.filter(
                category=self.category,
                name__iexact=self.name,  # insensible à la casse
                page_type__code=f"{self.category}_{key}"
            ).exists()
            
            if exists and key in base_urls:
                links.append(base_urls[key].format(slugified_name))
            else:
                links.append(None)
        # Ajout du lien forum (en dernière position)
        _ = self.get_forum_url  # force le calcul
        if template and template[-1] == "forum":
            links.append(self.get_forum_url if self.id_forum else None)
        else:
            links.append(None)
        return links

    def __str__(self):
        """Retourne le nom de l'entrée pour l'affichage dans Django Admin."""
        return self.name

class PageExistence(models.Model):
    """
    Modèle stockant les pages existantes pour éviter de les vérifier dynamiquement.
    Ce modèle est utilisé par l'index général et les index thématiques pour savoir
    si une page spécifique (biographie, discographie, etc.) existe avant d'afficher un lien.

    Chaque app (Artistes, Compilations, Labels...) mettra à jour cette table automatiquement.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Catégorie",
        help_text="Catégorie de l'entrée (artiste, compilation, label, lexique)."
    )
    name = models.CharField(
        max_length=255, verbose_name="Nom de l'entrée",
        help_text="Nom exact de l'entrée, utilisé pour générer les URL."
    )
    page_type = models.ForeignKey(
        PageType,
        on_delete=models.CASCADE,
        verbose_name="Type de page",
        help_text="Type de page existante (biographie, discographie, etc.)."
    )

    class Meta:
        # Empêche les doublons : chaque entrée doit être unique
        unique_together = ("category", "name", "page_type")
        indexes = [
            models.Index(fields=["category", "name", "page_type"]),  # 🔹 Index pour accélérer les recherches
        ]
        verbose_name = "Page existante"
        verbose_name_plural = "Index - Pages existantes"

    @cached_property
    def exists(self):
        """
        Renvoie True si cette page existe, False sinon.
        Utilise un cache pour éviter de refaire la requête à chaque appel.
        """
        return PageExistence.objects.filter(
            category=self.category, name=self.name, page_type=self.page_type
        ).exists()

    def __str__(self):
        """Affichage dans Django Admin et dans la console."""
        return f"{self.category} - {self.page_type} - {self.name}"

##====================================================
## Gestion de l'affichage des sous-lettres de l'index
##====================================================

class IndexSettings(models.Model):
    """
    Configuration pour afficher ou masquer les sous-lettres dans l'index général et les catégories.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
        help_text="Nom de la catégorie (ex: 'artistes', 'labels', etc.). Laisser vide pour l'index général."
    )
    apply_to_all = models.BooleanField(
        default=False,
        help_text="Cochez cette case pour activer les sous-lettres partout (toutes les lettres, chiffres et @)."
    )
    letters_with_sub_buttons = models.TextField(
        blank=True,
        help_text="Liste des lettres/chiffres activant les sous-lettres (ex: 'A,B,C,1,2,3')."
    )

    def get_active_letters(self):
        """Renvoie la liste des lettres/chiffres avec sous-lettres activés."""
        return self.letters_with_sub_buttons.split(",") if self.letters_with_sub_buttons else []

    def save(self, *args, **kwargs):
        if self.apply_to_all:
            self.letters_with_sub_buttons = "0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,@"
        super().save(*args, **kwargs)
        self.refresh_from_db()  # 🔹 Recharge l’objet depuis la base pour mettre à jour l'admin

    class Meta:
        unique_together = ("category",)
        indexes = [
            models.Index(fields=["category"]),  # 🔹 Accélère les requêtes par catégorie
        ]
        verbose_name = "Configuration de l'index"
        verbose_name_plural = "Index - Configuration"

    def __str__(self):
        return f"Config Index: {self.category.name if self.category else 'Index Général'}"
