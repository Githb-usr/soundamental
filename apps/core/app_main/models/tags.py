from django.db import models
from django.utils.text import slugify
from django.conf import settings

# ===========================
# 📂 MODÈLES POUR LES TAGS
# ===========================

class Tag(models.Model):
    """
    Modèle pour gérer les tags associés aux pages statiques et dynamiques.
    """
    ACCESS_LEVELS = settings.ACCESS_LEVELS
    ACCESS_LEVEL_CHOICES = [(v, k) for k, v in ACCESS_LEVELS.items()]

    name = models.CharField(max_length=255, unique=True, verbose_name="Nom du tag")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Description du tag")
    access_level = models.IntegerField(
        choices=ACCESS_LEVEL_CHOICES,
        default=ACCESS_LEVELS["public"],
        verbose_name="Niveau d'accès"
    )
    category = models.ForeignKey(
        "app_index.Category",           # référence lazy, pour éviter les problèmes d’import
        on_delete=models.SET_NULL,      # Conserver le tag même si la catégorie est supprimée
        null=True,
        blank=True,
        verbose_name="Catégorie liée"
    )

    class Meta:
        indexes = [
            models.Index(fields=["name"]),  # Accélère les recherches par nom
            models.Index(fields=["slug"]),  # Accélère les recherches par slug
        ]
        ordering = ["name"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags - Gestion globale"

    def save(self, *args, **kwargs):
        """
        Génère automatiquement un slug s'il n'est pas défini.
        """
        if not self.slug:
            self.slug = slugify(self.name)  # Génération automatique du slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  # Affichage correct avec majuscules
