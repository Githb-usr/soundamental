from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=True, cast=bool)
DEBUG_PROPAGATE_EXCEPTIONS = True
ENVIRONMENT = config('ENVIRONMENT', default='development')
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# En DEV on autorise localhost ; en PREPROD/PROD, production.py remplace via l'environnement.
if config('DEBUG', default=True, cast=bool):
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
else:
    ALLOWED_HOSTS = []  # Sera surchargé par production.py (ALLOWED_HOSTS depuis l'env)


# Autoriser les iframes depuis Calameo
CSP_FRAME_SRC = ("'self'", "https://v.calameo.com")
X_FRAME_OPTIONS = 'SAMEORIGIN'
# X_FRAME_OPTIONS = 'ALLOWALL'

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
