from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

class AppMainSettings(models.Model):
    """
    Stocke les paramètres globaux de l'application.
    """
    PARAMETER_CHOICES = (
        ("nb_max_modifs", "Nombre max de modifications sauvegardées"),
    )
    
    def save(self, *args, **kwargs):
        """
        Sauvegarde le paramètre et met à jour le cache.
        """
        update_cache = kwargs.pop("update_cache", True)  # 🔹 Extrait update_cache, True par défaut

        super().save(*args, **kwargs)  # 🔹 Sauvegarde sans problème

        if update_cache:  # 🔹 Met à jour le cache seulement si demandé
            cache.set(f"app_main_setting_{self.name}", self.value, timeout=3600)

    name = models.CharField(max_length=255, unique=True, choices=PARAMETER_CHOICES)
    value = models.IntegerField(default=10)

    @staticmethod
    def get_value(param_name, default=None):
        """
        Récupère la valeur d'un paramètre global avec mise en cache.
        """
        cache_key = f"app_main_setting_{param_name}"
        value = cache.get(cache_key)

        if value is None:  # Si la valeur n'est pas en cache, on la récupère en base
            param = AppMainSettings.objects.filter(name=param_name).first()
            value = param.value if param else default
            cache.set(cache_key, value, timeout=3600)  # Stocke la valeur en cache pendant 1h

        return value

    def __str__(self):
        return f"{self.name}: {self.value}"

@receiver(post_save, sender=AppMainSettings)
def update_cache_on_save(sender, instance, **kwargs):
    """
    Met à jour le cache à chaque sauvegarde d'un paramètre.
    """
    cache.set(f"app_main_setting_{instance.name}", instance.value, timeout=3600)
