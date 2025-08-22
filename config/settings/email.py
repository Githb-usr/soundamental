from decouple import config, Csv

# Configuration des administrateurs
ADMINS = config("ADMINS", default="", cast=Csv())  # Pas de valeur par défaut pour préserver l'adresse mail principale
ADMINS = [tuple(admin.split(":")) for admin in ADMINS]  # Évite les erreurs si vide

# Configuration des mails
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
