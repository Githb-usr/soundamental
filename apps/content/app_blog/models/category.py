# apps/content/app_blog/models/category.py
from django.db import models
from django.utils.text import slugify

class CategorieArticle(models.Model):
    nom = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nom court de la catégorie, affiché dans les formulaires et les listes."
    )
    description = models.TextField(
        blank=True,
        help_text="Description de la catégorie : explique ce qu'elle regroupe. Affichée dans l'admin pour aider à faire le bon choix."
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        help_text="Slug généré automatiquement à partir du nom si laissé vide."
    )
 
    class Meta:
        verbose_name = "Catégorie d'article"
        verbose_name_plural = "Catégories d'article"
        ordering = ['nom']

    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)
