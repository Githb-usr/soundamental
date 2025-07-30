from decouple import Config, RepositoryEnv

# Structures des principaux liens de Soundamental
LINK_BASES = {
    "forum": "https://www.soundamental.org/forum/topic/{}",

    "artiste": {
        "biography" : "https://www.soundamental.org/artistes/{}", # Biographie
        "discography": "https://www.soundamental.org/artistes/{}/discographie",
		"detailed_discography": "https://www.soundamental.org/artistes/{}/discographie-detaillee",
        "videography": "https://www.soundamental.org/artistes/{}/videographie",
		"detailed_videography": "https://www.soundamental.org/artistes/{}/videographie-detaillee",
        "bootography": "https://www.soundamental.org/artistes/{}/bootographie",
		"detailed_bootography": "https://www.soundamental.org/artistes/{}/bootographie-detaillee",
        "repertoire": "https://www.soundamental.org/artistes/{}/repertoire",
		"others": "https://www.soundamental.org/artistes/{}/autres-supports",
    },
    "compilation": {
        "history": "https://www.soundamental.org/compilations/{}", # Historique
        "volumes": "https://www.soundamental.org/compilations/{}/volumes",
        "videography": "https://www.soundamental.org/compilations/{}/videographie",
		"detailed_videography": "https://www.soundamental.org/compilations/{}/videographie-detaillee",
        "bootography": "https://www.soundamental.org/compilations/{}/bootographie",
		"detailed_bootography": "https://www.soundamental.org/compilations/{}/bootographie-detaillee",
		"detailed_volumes": "https://www.soundamental.org/compilations/{}/volumes-detailles",
    },
    "label": {
        "history": "https://www.soundamental.org/labels/{}", # Historique
        "catalog": "https://www.soundamental.org/labels/{}/catalogue",
        "bootography": "https://www.soundamental.org/labels/{}/bootographie",
		"detailed_bootography": "https://www.soundamental.org/labels/{}/bootographie-detaillee",
		"detailed_catalog": "https://www.soundamental.org/labels/{}/catalogue-detaille",
    },
}

# Codes des liens de l'index
INDEX_LINK_CODES = {
    "biography": "BIO",  # Biographie (Artistes)
    "history": "HIS",  # Historique (Compilations, Labels)
    "discography": "DIS",  # Discographie (Artistes)
    "volumes": "VOL",  # Volumes (Compilations)
    "catalog": "CAT",  # Catalogue (Labels)
    "videography": "VID",  # Vidéographie (Artistes)
    "bootography": "BOO",  # Bootographie (Artistes)
    "forum": "FOR",  # Forum (toutes catégories)
}

# Ce mapping définit, pour chaque catégorie d'entrée de l'index,
# la liste des types de pages qui peuvent être liées dans l'interface.
# - La clé est le code interne de la catégorie (ex: "artiste", "genre_musical", ...).
# - La valeur est une liste de 5 éléments : chaque position correspond à un type de page
#   (ou None si non utilisé), la dernière position doit être "forum" si un lien forum existe.
# Exemple :
#   "artiste": ["biography", "discography", "videography", "bootography", "forum"]
# ➔ Si tu ajoutes une nouvelle catégorie, AJOUTE-LA ICI obligatoirement,
#   sinon les liens ne s’afficheront pas dans l’index.
INDEX_LINK_TEMPLATES = {
    "artiste": ["biography", "discography", "videography", "bootography", "forum"],
    "compilation": ["history", "volumes", "videography", "bootography", "forum"],
    "label": ["history", "catalog", None, "bootography", "forum"],
    "lexique": ["definition", None, None, None, "forum"],
    "animateur_radio": [None, None, None, None, "forum"],
    "chaine_tv": [None, None, None, None, "forum"],
    "club": [None, None, None, None, "forum"],
    "collection": [None, None, None, None, "forum"],
    "documentaire": [None, None, None, None, "forum"],
    "emission_radio": [None, None, None, None, "forum"],
    "emission_tv": [None, None, None, None, "forum"],
    "emission_web": [None, None, None, None, "forum"],
    "film": [None, None, None, None, "forum"],
    "genre_musical": [None, None, None, None, "forum"],
    "jeu_video": [None, None, None, None, "forum"],
    "livre": [None, None, None, None, "forum"],
    "magazine": [None, None, None, None, "forum"],
    "pub_tv": [None, None, None, None, "forum"],
    "reportage": [None, None, None, None, "forum"],
    "serie": [None, None, None, None, "forum"],
    "site_web": [None, None, None, None, "forum"],
    "station_radio": [None, None, None, None, "forum"],
    "webradio": [None, None, None, None, "forum"],
}

# Ce mapping sert uniquement à générer les URL de navigation pour les index thématiques.
# - La clé est le nom affiché au pluriel de la catégorie (ex: "artistes", "compilations").
# - La valeur est le code utilisé dans l’URL pour cette catégorie (ex: "artiste", "compilation").
# ➔ À compléter UNIQUEMENT si la nouvelle catégorie doit avoir sa propre page d’index thématique
#   (ex : index des artistes, index des labels, etc.).
# ➔ Inutile pour les catégories "secondaires" ou techniques non visibles dans l’index global.

# Pour les noms composés de plusieurs mots, la clé doit être identique
# à la forme plurielle affichée sur le site (ex: "sites internet / applications"),
# et la valeur doit correspondre au code technique de la catégorie (ex: "site_internet_application").
CATEGORY_MAPPING = {
    "artistes": "artiste",
    "collection": "collection",
    "compilations": "compilation",
    "labels": "label",
    "lexique": "lexique"
}