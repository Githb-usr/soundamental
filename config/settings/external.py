from decouple import config
import socket
from decouple import Config, RepositoryEnv

# TinyMCE Configuration
TINYMCE_DEFAULT_CONFIG = {
    "height": 400,
    "width": "100%",
    "language": "fr_FR",
    "language_url": "/static/js/tinymce/langs/fr_FR.js",
    "plugins": [
    'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview', 'anchor',
    'searchreplace', 'visualblocks', 'code', 'fullscreen', 'insertdatetime', 'media',
    'table', 'help', 'wordcount'
    ],
    "toolbar":
    'undo redo | formatselect fontselect fontsizeselect | ' +
    'bold italic underline strikethrough | forecolor backcolor | ' +
    'alignleft aligncenter alignright alignjustify | ' +
    'bullist numlist outdent indent | ' +
    'link image media table | browseImage uploadImageFromSite | code fullscreen preview',
    "menubar": "file edit view insert format tools table help",
    "statusbar": True,
}

# Bibliothèques d’images disponibles pour insertion dans TinyMCE
IMAGES_BIBLIOTHEQUES = {
    "blog": {
        "label": "Images du blog",
        "path": "blog",
    },
    "site": {
        "label": "Images du site",
        "path": "site",
    },
    "downloads": {
        "label": "Images des fichiers à télécharger",
        "path": "downloads",  # on cible uniquement les images
    },
    # Tu pourras en ajouter d'autres plus tard
}


# Active reCAPTCHA uniquement en production
IS_LOCAL = socket.gethostname() in ["localhost", "127.0.0.1"]
if IS_LOCAL:
    RECAPTCHA_PUBLIC_KEY = "test"
    RECAPTCHA_SECRET_KEY = "test"
else:
    # reCAPTCHA
    RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')
# Définissant du domaine reCAPTCHA
RECAPTCHA_DOMAIN = "www.google.com"
