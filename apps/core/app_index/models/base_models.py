from django.db import models

# ========================
# Modèles de base (catégories)
# ========================

class Category(models.Model):
    """
    Modèle représentant une catégorie pour les entrées de l'index.
    """
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code",
        help_text="Clé technique unique (ex: artiste, compilation, label, lexique, etc.)."
    )
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nom",
        help_text="Nom de la catégorie (ex: Artiste, Label, Compilation)."
    )
    label = models.CharField(
        max_length=100,
        verbose_name="Libellé affiché (au pluriel, si besoin)"
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Description",
        help_text="Description de la catégorie."
    )

    @property
    def plural_label(self):
        """
        Libellé au pluriel. Utiliser quand on veut explicitement le pluriel
        (menus, titres de sections, etc.). Évite les ambiguïtés côté template.
        """
        return self.label

    def __str__(self):
        """
        Représentation texte par défaut de Category.
        On force le singulier pour l’admin et partout où Django affiche l’objet.
        """
        return self.name

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Index - Catégories"
        ordering = ["name"]


class PageType(models.Model):
    """
    Modèle représentant un type de page pour les entrées de l'index.
    """
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Code technique",
        help_text="Identifiant technique, utilisé dans le code (ex: artiste_biography, label_history)."
    )
    label = models.CharField(
        max_length=100,
        verbose_name="Nom affiché",
        help_text="Nom affiché du type de page (ex: Biographie (Artistes))."
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Description",
        help_text="Description du type de page."
    )

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Type de page"
        verbose_name_plural = "Index - Types de pages"
        ordering = ["label"]
