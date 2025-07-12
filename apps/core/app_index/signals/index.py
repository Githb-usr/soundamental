from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.core.app_index.models import PageExistence, IndexEntry

@receiver(post_save, sender=PageExistence)
def create_index_entry(sender, instance, created, **kwargs):
    """Crée une entrée dans IndexEntry quand une nouvelle page est ajoutée à PageExistence."""
    if created:  # On ne fait ça que pour les nouvelles entrées
        IndexEntry.objects.get_or_create(
            name=instance.name,
            defaults={"category": instance.category}
        )

@receiver(post_delete, sender=PageExistence)
def delete_index_entry(sender, instance, **kwargs):
    """Supprime une entrée de IndexEntry si la dernière page associée à cet artiste/label/compilation est supprimée."""
    if not PageExistence.objects.filter(name=instance.name).exists():  # Vérifie si d'autres pages existent encore
        IndexEntry.objects.filter(name=instance.name).delete()
