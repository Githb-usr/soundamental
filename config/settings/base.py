import os
import sys
from pathlib import Path
from decouple import AutoConfig  # lit d'abord os.environ, puis .env si présent

from .email import *
from .external import *
from .project import *
from .security import *
from .test import *

# Définition du répertoire racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# AutoConfig : priorité à os.environ ; fallback sur .env si présent à la racine du projet
config = AutoConfig(search_path=BASE_DIR)

# Variables d'environnement
ENVIRONMENT = config("ENVIRONMENT", default="local")

# Force Django à trouver les packages installés dans le venv
sys.path.insert(0, os.path.join(BASE_DIR, "venv", "Lib", "site-packages"))

# Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_recaptcha',
    'import_export',
    'django_select2',
    'django.contrib.syndication',
    'apps.core.app_index',
    'apps.core.app_main',
    'apps.core.app_medias',
    'apps.core.app_search',
    'apps.content.app_artistes',
    'apps.content.app_blog',
    'apps.content.app_pressages',    
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Templates & URLs
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "templates/pages"),  # Ajout pour que Django trouve "static_page.html"
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Internationalisation
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [('fr', 'Français')]
DATE_FORMAT = "d F Y"
DATETIME_FORMAT = "d F Y H:i"
TIME_FORMAT = "H:i"

# Fichiers statiques & médias
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Clé par défaut pour les modèles
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Taille de pagination par défaut pour tout le projet (modifiable lors de 'lappel de la fonction)
PAGINATION_SIZE = 25

# Délai par défaut entre deux requêtes utilisateur sensibles (ex: contact)
DEFAULT_REQUEST_DELAY = 120  # 120 secondes (2 minutes)

# Redirections après connexion et déconnexion
LOGIN_REDIRECT_URL = "app_main:home"
LOGOUT_REDIRECT_URL = "app_main:home"

# Droits d'accès globaux
ACCESS_LEVELS = {
    "public": 1,
    "registered": 2,
    "moderator": 3,
    "admin": 4,
}

# MIGRATION_MODULES = {
#     "app_main": None,  # 🔹 Désactive les migrations pour `app_main`
# }
