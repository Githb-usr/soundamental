import os
from django.core.wsgi import get_wsgi_application
from decouple import config

ENVIRONMENT = config("ENVIRONMENT", default="local")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{ENVIRONMENT}")

application = get_wsgi_application()
