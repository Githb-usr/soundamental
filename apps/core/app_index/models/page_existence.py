from django.db import models
from django.utils.functional import cached_property
from .base_models import Category, PageType

# ==========================================
# Pages existantes (présence de pages liées)
# ==========================================

class PageExistence(models.Model):
    """
    Modèle stockant les pages existantes pour éviter de les vérifier dynamiquement.
    Ce modèle est utilisé par l'index général et les index thématiques pour savoir
    si une page spécifique (biographie, discographie, etc.) existe avant d'afficher un lien.

    Chaque app (Artistes, Compilations, Labels...) mettra à jour cette table automatiquement.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Catégorie",
        help_text="Catégorie de l'entrée (artiste, compilation, label, lexique)."
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Nom de l'entrée",
        help_text="Nom exact de l'entrée, utilisé pour générer les URL."
    )
    page_type = models.ForeignKey(
        PageType,
        on_delete=models.CASCADE,
        verbose_name="Type de page",
        help_text="Type de page existante (biographie, discographie, etc.)."
    )

    class Meta:
        unique_together = ("category", "name", "page_type")
        indexes = [
            models.Index(fields=["category", "name", "page_type"]),
        ]
        verbose_name = "Page existante"
        verbose_name_plural = "Index - Pages existantes"

    @cached_property
    def exists(self):
        """
        Renvoie True si cette page existe, False sinon.
        Utilise un cache pour éviter de refaire la requête à chaque appel.
        """
        return PageExistence.objects.filter(
            category=self.category, name=self.name, page_type=self.page_type
        ).exists()

    def __str__(self):
        return f"{self.category} - {self.page_type} - {self.name}"
