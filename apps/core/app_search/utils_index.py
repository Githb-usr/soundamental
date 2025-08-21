# apps/core/app_search/utils_index.py
# (extraits déplacés depuis views.py — inchangés)

from unidecode import unidecode

# --- Sous-filtres pour la recherche "index" ---
# Mappe les libellés de filtres UI → codes de catégories en base.
# ⚠ Adapte les codes si besoin (ex.: "artists" vs "artistes")
INDEX_SUBFILTERS: dict[str, set[str]] = {
    "tout": set(),               # aucun filtre → toutes catégories d'index
    "artistes": {"artiste"},
    "compilations": {"compilation"},
    "labels": {"label"},
}

def _codes_for_index_type(index_type: str) -> set[str] | None:
    """
    Normalise 'index_type' et renvoie l'ensemble des codes de catégorie à filtrer.
    Retourne None si aucun filtre (cas 'tout').
    """
    idx = (index_type or "tout").strip().lower()
    codes = INDEX_SUBFILTERS.get(idx, set())
    return None if not codes else codes

def _first_letter(name: str) -> str:
    """
    Première lettre normalisée :
      - A..Z → cette lettre
      - 0..9 → ce chiffre (⚠ pas de sous-lettres pour chiffres)
      - sinon → '@' (rubrique 'Autres')
    """
    s = unidecode((name or "").strip())
    if not s:
        return "@"
    ch = s[0].upper()
    if "A" <= ch <= "Z":
        return ch
    if ch.isdigit():
        return ch
    return "@"

def _sub_letter_alpha(name: str) -> str | None:
    """
    Sous-lettre = 2 premières lettres A..Z du nom (normalisé).
    Ex : 'Michael' → 'MI', 'Mötley' → 'MO'. Retourne None si indisponible.
    """
    letters = [c.upper() for c in unidecode(name or "") if "A" <= c.upper() <= "Z"]
    if len(letters) >= 2:
        return "".join(letters[:2])
    return None

# Petit cache mémoire pour éviter de requêter IndexSettings à chaque entrée
_SUB_CFG_CACHE: dict[int | str, set[str]] = {}

def _active_subletters_for(category_obj) -> set[str]:
    """
    Renvoie l’ensemble des lettres (A..Z) pour lesquelles les sous-lettres sont activées,
    en tenant compte de la configuration spécifique à la catégorie OU générale (category=None).
    - On ignore volontairement les chiffres et '@' (pas de sous-lettres pour eux).
    """
    from apps.core.app_index.models.config_index import IndexSettings  # import local

    key = category_obj.id if category_obj else "general"
    if key in _SUB_CFG_CACHE:
        return _SUB_CFG_CACHE[key]

    # 1) On privilégie la config propre à la catégorie si elle existe
    cfg = IndexSettings.objects.filter(category=category_obj).first()
    # 2) À défaut, on utilise la config générale (category IS NULL) s’il y en a une
    if not cfg:
        cfg = IndexSettings.objects.filter(category__isnull=True).first()

    if not cfg:
        _SUB_CFG_CACHE[key] = set()
        return _SUB_CFG_CACHE[key]

    if cfg.apply_to_all:
        active = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # partout (mais pas chiffres/@)
    else:
        # On nettoie la liste fournie, on garde uniquement A..Z
        raw = cfg.get_active_letters()
        active = {t.strip().upper() for t in raw if t.strip() and t.strip().upper().isalpha()}

    _SUB_CFG_CACHE[key] = active
    return active
