from decouple import config, Csv
from .base import *
from .database import DATABASES
from .security import *
from .email import *
from .external import *
from .project import *
import os

# Mode production
DEBUG = False

# ALLOWED_HOSTS lu depuis les variables d'environnement (o2switch)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

# (optionnel mais recommandé) CSRF depuis l'env aussi
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="", cast=Csv())

# Active la compression des fichiers statiques
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# Email via SMTP
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Sécurité renforcée
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_SSL_REDIRECT = True
SECURE_SSL_REDIRECT = False #temporaire pour tests / debug
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django-errors.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
