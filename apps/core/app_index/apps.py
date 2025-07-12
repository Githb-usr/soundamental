import sys
from django.conf import settings
from django.apps import AppConfig

class AppIndexConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core.app_index'

    def ready(self):
        if "pytest" in sys.modules or getattr(settings, "DISABLE_SIGNALS", False):
            return
        
        import apps.core.app_index.signals.index
