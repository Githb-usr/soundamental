from .base import *
from .database import DATABASES
from .security import *
from .email import *
from .external import *
from .project import *
from decouple import Config, RepositoryEnv

# Mode développement
DEBUG = True

# Active les outils de développement (ex: debug toolbar)
INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")

# Email en mode dev (envoi de vrais mails pour vérif)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Django Debug Toolbar autorisé localement uniquement
INTERNAL_IPS = ["127.0.0.1"]
