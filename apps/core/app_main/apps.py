import sys
from django.conf import settings
from django.apps import AppConfig

class AppMainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core.app_main'

    def ready(self):
        """Charge les signaux de l'application, sauf si on est en mode test."""
        if "pytest" in sys.modules or getattr(settings, "DISABLE_SIGNALS", False):
            return  # 🔹 Ne charge pas les signaux en mode test

        import apps.core.app_main.signals.settings
