from .base import *
from .database import DATABASES
from .security import *
from .email import *
from .external import *
from .project import *
from decouple import Config, RepositoryEnv

# Mode production
DEBUG = False
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "soundamental.org", "www.soundamental.org"]

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
