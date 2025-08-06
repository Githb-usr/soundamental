from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from apps.core.app_main.models.tags import Tag
from apps.core.app_main.models.settings import AppMainSettings

# ===================
# 📂 PAGES STATIQUES
# ===================

CATEGORY_CHOICES = [
        ("site-info", "Pages de base"),
        ("aide", "Pages Aide/FAQ"),
]

class StaticPageMeta(models.Model):
    """
    Modèle principal des pages statiques.
    Ajout de la gestion de l'historique des 10 dernières versions.
    """
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)  # Généré automatiquement si vide
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="custom",
        verbose_name="Catégorie",
        help_text="Permet de trier les pages selon leur usage"
    )
    content = models.TextField(
        help_text="Contenu de la page (mise en forme avec TinyMCE)."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)  # Page publiée ou non
    tags = models.ManyToManyField(Tag, blank=True, related_name="static_pages")  # Ajout des tags ici

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_static_pages")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="updated_static_pages")

    class Meta:
        ordering = ["title"]
        verbose_name = "Page statique"
        verbose_name_plural = "Pages statiques"
        indexes = [
            models.Index(fields=["slug"]),  # 🔹 Accélère les recherches par slug
        ]

    def save(self, *args, **kwargs):
        """
        Sauvegarde la modification et gère l'historique des versions.
        Optimisation : Ne génère un slug que si le titre change.
        """
        # if not self.slug or (self.pk and StaticPageMeta.objects.get(pk=self.pk).title != self.title):
        #     self.slug = slugify(self.title)  # Génération uniquement si nécessaire
        # super().save(*args, **kwargs)  # Sauvegarde normale
        # StaticPageHistory.save_modification(self)
        is_update = self.pk is not None

        if not self.slug or (is_update and StaticPageMeta.objects.get(pk=self.pk).title != self.title):
            self.slug = slugify(self.title)

        # Vérification avant sauvegarde
        has_changed = self.has_changed() if is_update else True

        super().save(*args, **kwargs)

        # Si cette sauvegarde est déclenchée via l’admin à cause d’une suppression → ne rien faire
        if not getattr(self, '_skip_save_modification', False) and is_update and has_changed:
            StaticPageHistory.save_modification(self)
   
    def has_changed(self):
        """
        Compare les valeurs actuelles avec celles en base pour détecter une modification réelle.
        """
        if not self.pk:
            return True  # Nouvelle instance

        try:
            db_instance = StaticPageMeta.objects.get(pk=self.pk)
        except StaticPageMeta.DoesNotExist:
            return True

        # Liste des champs à surveiller
        fields_to_check = ["title", "slug", "category", "content", "published"]

        for field in fields_to_check:
            current_value = getattr(self, field)
            db_value = getattr(db_instance, field)
            if current_value != db_value:
                return True

        return False


    def get_absolute_url(self):
        """
        Retourne l'URL absolue de la page statique.
        """
        return f"/{self.slug}/"

    def __str__(self):
        return self.title

# =========================================
# 📂 MODÈLES POUR TRACER LES MODIFICATIONS
# =========================================

class StaticPageHistory(models.Model):
    """
    Historique des modifications des pages statiques (on conserve les 10 dernières).
    """
    page = models.ForeignKey(StaticPageMeta, on_delete=models.SET_NULL, related_name="history", null=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-modified_at"]
        indexes = [
            models.Index(fields=["modified_at"]),  # 🔹 Accélère les requêtes sur l'historique
        ]
        verbose_name = "Historique de la page statique"
        verbose_name_plural = "Pages statiques - Historiques"

    @staticmethod
    def save_modification(page_instance):
        """
        Ajoute une modification à l'historique et conserve uniquement les 10 dernières.
        """
        max_history = AppMainSettings.get_value("nb_max_modifs", 10)

        # Crée la nouvelle entrée
        StaticPageHistory.objects.create(
            page=page_instance, 
            modified_by=page_instance.updated_by
        )

        # Récupère les IDs des entrées à supprimer (au-delà de la limite)
        excess_entries = StaticPageHistory.objects.filter(page=page_instance)\
                            .order_by('-modified_at')[max_history:]

        # Correction importante : utilise une liste explicite d'IDs
        excess_entry_ids = [entry.id for entry in excess_entries]
        
        # Supprime effectivement les entrées excédentaires
        if excess_entry_ids:
            StaticPageHistory.objects.filter(id__in=excess_entry_ids).delete()
            print("Suppression effectuée.")
        else:
            print("Aucune suppression nécessaire.")
