import pytest
from django.db.models.signals import post_save
from apps.core.app_main.models import AppMainSettings
from apps.core.app_main.signals.settings import update_cache_on_save

@pytest.fixture(autouse=True)
def disable_signals():
    """Désactive proprement les signaux `post_save` pour éviter d'affecter les tests."""
    # Désactiver uniquement le signal concerné (et pas tous les signaux Django !)
    post_save.disconnect(update_cache_on_save, sender=AppMainSettings)

    yield  # Exécute le test

    # Réactive le signal après le test
    post_save.connect(update_cache_on_save, sender=AppMainSettings)
