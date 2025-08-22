import os
from .base import *
from .security import *
from .email import *
from .external import *
from .project import *
from decouple import config

# Désactiver le debug pour ne pas polluer les tests
DEBUG = False
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Désactiver les signaux pour ne pas polluer les tests
DISABLE_SIGNALS = False

# Base de données de test (MySQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "test_soundamental",
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", cast=int),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        "TEST": {
            "NAME": "test_soundamental",
        },
    }
}

# Réduit les logs pour les tests
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
}

# Accélération des tests (pas de password hashing lourd)
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

TEST_MODE = os.environ.get("TEST_MODE", "False") == "True"
