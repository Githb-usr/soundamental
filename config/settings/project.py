from decouple import Config, RepositoryEnv

# Liste des pages statiques bien définie pour éviter les conflits
STATIC_PAGES = [
    "accueil", 
    "confirmation-envoi-message", 
    "a-propos-de-soundamental", 
    "politique-de-confidentialite", 
    "avertissements", 
    "liens",
    "charte-du-forum",
]

DYNAMIC_RESERVED_NAMES = [
    "index",
    "telechargements",
]

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

CATEGORY_MAPPING = {
    "artistes": "artiste",
    "compilations": "compilation",
    "labels": "label",
    "lexique": "lexique"
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

INDEX_LINK_TEMPLATES = {
    "artiste": ["biography", "discography", "videography", "bootography", "forum"],
    "compilation": ["history", "volumes", "videography", "bootography", "forum"],
    "label": ["history", "catalog", None, "bootography", "forum"],
    "lexique": ["definition", None, None, None, "forum"],
}
