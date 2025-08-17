from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from unidecode import unidecode

from .base_models import Category
from .page_existence import PageExistence

# ===============================
# Entrée principale de l'index
# ===============================

class IndexEntry(models.Model):
    """
    Modèle représentant une entrée de l'index général et thématique.
    - Une entrée correspond à un artiste, un label, une compilation, etc.
    - Les entrées sont générées dynamiquement, mais certaines infos (comme l'ID du forum) doivent être stockées.
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Nom",
        help_text="Nom officiel de l'entrée (ex: Michael Jackson, Top DJ Hits)"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Catégorie",
        help_text="Type d'entrée (artiste, compilation, label, etc.)"
    )
    id_forum = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="ID Forum",
        help_text="ID du forum sous la forme '12345-slug' (ex: 9699-stereotype)"
    )

    class Meta:
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["name"]),
        ]
        ordering = ["name"]
        verbose_name = "Entrée de l'index"
        verbose_name_plural = "Index - Entrées"

    @cached_property
    def get_forum_url(self):
        """
        Génère et met en cache l'URL du forum pour cette entrée si un ID forum est renseigné.
        Exemple :
            id_forum = "12345-stereotype"
            ➝ Retourne : "https://www.soundamental.org/forum/topic/12345-stereotype"
        """
        return settings.LINK_BASES["forum"].format(self.id_forum) if self.id_forum else None

    @cached_property
    def get_links(self):
        """
        Génère la liste des liens disponibles pour l'entrée, en fonction des pages existantes.
        La logique s'appuie sur LINK_BASES et INDEX_LINK_TEMPLATES dans les settings.
        """
        base_urls = settings.LINK_BASES.get(self.category.code, {})
        template = settings.INDEX_LINK_TEMPLATES.get(self.category.code, [None] * 5)
        slugified_name = f"{self.id}-{unidecode(self.name).lower().replace(' ', '-')}"
        links = []

        for key in template[:-1]:  # on gère forum à part
            if not key:
                links.append(None)
                continue

            exists = PageExistence.objects.filter(
                category=self.category,
                name__iexact=self.name,  # insensible à la casse
                page_type__code=f"{self.category}_{key}"
            ).exists()

            if exists and key in base_urls:
                links.append(base_urls[key].format(slugified_name))
            else:
                links.append(None)

        # Ajout du lien forum (en dernière position)
        _ = self.get_forum_url  # force le calcul
        if template and template[-1] == "forum":
            links.append(self.get_forum_url if self.id_forum else None)
        else:
            links.append(None)

        return links

    def __str__(self):
        return self.name
