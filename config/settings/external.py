from decouple import config
import socket
from decouple import Config, RepositoryEnv

# TinyMCE Configuration
# Options communes (public/admin)
TINYMCE_COMMON_CONFIG = {
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
    "content_style": "body { font-family: Arial,Helvetica,sans-serif; font-size:14px }",
    "fontsize_formats": "8pt 10pt 12pt 14pt 16pt 18pt 24pt 36pt 48pt",
}

# Config ADMIN : permissive (usage interne uniquement)
TINYMCE_ADMIN_CONFIG = {
    **TINYMCE_COMMON_CONFIG,
    "extended_valid_elements": "*[*]",  # Autorise tous les attributs sur toutes les balises
    "valid_elements":
        "p,br,ul,ol,li,div[style],span[style],b,strong,i,em,u,sup,sub,"
        "h1,h2,h3,h4,h5,h6,blockquote,pre,code,"
        "a[href|title|target|rel],"
        "img[src|alt|title|width|height|style],"
        "table,tr,td,th,thead,tbody,tfoot,"
        "hr",
    "valid_styles": {
        '*': 'float,width,height,margin,margin-top,margin-bottom,margin-left,margin-right,'
             'padding,padding-top,padding-bottom,padding-left,padding-right,display,border,'
             'border-radius,background,background-color,background-image,text-align,'
             'vertical-align,position,top,left,right,bottom,font-size,font-family,color',
    },
}

# Config PUBLIC : options restreintes, pas de balises dangereuses, styles limités
TINYMCE_PUBLIC_CONFIG = {
    **TINYMCE_COMMON_CONFIG,
    "valid_elements":
        "p,br,ul,ol,li,b,strong,i,em,u,sup,sub,"
        "h1,h2,h3,h4,h5,h6,blockquote,pre,code,"
        "a[href|title|target|rel],"
        "img[src|alt|title|width|height],"
        "table,tr,td,th,thead,tbody,tfoot,"
        "hr",
    "valid_styles": {
        '*': 'font-size,font-family,text-align,color',
    },
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
