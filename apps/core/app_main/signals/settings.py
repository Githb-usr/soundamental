from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from apps.core.app_main.models import AppMainSettings

@receiver(post_save, sender=AppMainSettings)
def update_cache_on_save(sender, instance, **kwargs):
    """Met à jour le cache à chaque sauvegarde d'un paramètre, sauf si les signaux sont désactivés."""
    if getattr(settings, "DISABLE_SIGNALS", False):
        return  # 🔹 Désactive le signal en mode test

    cache.set(f"app_main_setting_{instance.name}", instance.value, timeout=3600)
