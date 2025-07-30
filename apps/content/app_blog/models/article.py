# apps/content/app_blog/models/article.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.conf import settings
from PIL import Image

from .category import CategorieArticle
from ..defaults import BLOG_IMAGE_MAX_WIDTH, BLOG_IMAGE_JPEG_QUALITY
from apps.core.app_main.models.tags import Tag

User = get_user_model()


class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(est_publie=True)


class Article(models.Model):
    """
    Modèle représentant un article de blog publié sur Soundamental.
    """
    titre = models.CharField(
        max_length=200,
        help_text="Titre de l'article (affiché dans la liste et sur la page)."
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        help_text="Généré automatiquement à partir du titre si vide."
    )

    resume = models.TextField(
        blank=True,
        help_text="Résumé de l'article. S'affiche dans les aperçus. Si vide, un extrait automatique sera utilisé."
    )

    contenu = models.TextField(
        help_text=("Contenu principal de l’article (avec mise en forme TinyMCE).")
    )

    image = models.ImageField(
        upload_to='blog/illustrations/',
        blank=True,
        null=True,
        help_text=(
            "Image d'illustration de l'article. "
            "Elle sera automatiquement redimensionnée à une largeur maximale de 1200 px "
            "et compressée (qualité 85 %). Préférez une image d’au moins 1200 px de large."
            "Une image plus petite ne sera pas redimensionnée."
        )
    )
    
    # apps/content/app_blog/models/article.py

    masquer_image = models.BooleanField(
        default=False,
        verbose_name="Ne pas afficher l'image d'illustration dans l'article",
        help_text="Cochez pour masquer l'image d'illustration en haut de l'article (elle reste utilisée pour la liste d'articles)."
    )

    auteur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Utilisateur ayant rédigé l'article."
    )
    
    date_publication = models.DateTimeField(
        null=True,
        db_index=True,
        help_text="Date initiale de publication."
    )

    date_modification = models.DateTimeField(
        auto_now=True,
        help_text="Date de dernière modification."
    )

    est_publie = models.BooleanField(
        default=False,
        help_text="L'article est-il visible publiquement ?"
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="articles",
        help_text="Tags associés à cet article (navigation par thème)."
    )
    
    categorie_principale = models.ForeignKey(
        CategorieArticle,
        on_delete=models.PROTECT,
        related_name="articles_avec_cette_categorie_principale",
        help_text="Catégorie principale de l’article.",
        null=True,  # ← temporaire pour débloquer
    )

    categories_secondaires = models.ManyToManyField(
        CategorieArticle,
        blank=True,
        related_name="articles_avec_cette_categorie_secondaire",
        help_text="Catégories secondaires (optionnelles).",
    )
    
    objects = ArticleQuerySet.as_manager()

    class Meta:
        ordering = ['-date_publication']
        get_latest_by = 'date_publication'
        verbose_name = "Article de blog"
        verbose_name_plural = "Blog - Articles"
        
    def get_resume(self):
        """
        Retourne le résumé défini manuellement, ou un extrait du contenu.
        """
        if self.resume:
            return self.resume
        # Génère un extrait HTML propre si le résumé est vide
        from django.utils.html import strip_tags
        return strip_tags(self.contenu)[:300] + "..."

    def __str__(self):
        return self.titre
    
    @classmethod
    def generate_slug(cls, instance):
        """
        Génère un slug unique basé sur le titre de l’article.
        """
        if not hasattr(instance, "titre"):
            raise TypeError("L'argument fourni à generate_slug() doit être une instance d'Article, pas une chaîne.")

        base_slug = slugify(instance.titre)[:100]
        slug = base_slug
        suffix = 1

        while cls.objects.filter(slug=slug).exists():
            suffix += 1
            slug = f"{base_slug}-{suffix}"

        return slug
    
    def get_image_url(self):
        """
        Retourne l'URL de l'image à afficher pour cet article.
        Peut être modifiée plus tard pour intégrer une image mutualisée.
        """
        if self.image:
            return self.image.url
        return None

    def save(self, *args, **kwargs):
        # Slug automatiquement généré si vide
        if not self.slug and self.titre:
            base_slug = slugify(self.titre)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

        # Redimensionnement et compression de l'image d'illustration
        if self.image:
            image_path = self.image.path
            with Image.open(image_path) as img:
                max_width = BLOG_IMAGE_MAX_WIDTH
                quality = BLOG_IMAGE_JPEG_QUALITY

                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")  # conversion obligatoire pour JPEG

                # Resize uniquement si largeur > max_width
                if img.width > max_width:
                    ratio = max_width / float(img.width)
                    new_height = int(float(img.height) * ratio)
                    img = img.resize((max_width, new_height), Image.LANCZOS)
                    resized = True
                else:
                    resized = False

                # Sauvegarde avec compression systématique (même sans redimensionnement)
                img.save(image_path, optimize=True, quality=quality)

                # Marque que l’image a été modifiée (pour affichage dans l’admin ensuite)
                self._image_traitement_info = (
                    f"Image redimensionnée à {max_width}px (qualité {quality}%)"
                    if resized else f"Image compressée sans redimensionnement (qualité {quality}%)"
                )

    def clean(self):
        """
        Validation du modèle : s’assure que les contraintes métiers sont respectées.
        """
        # Si l'article est publié, il doit obligatoirement avoir une date de publication
        if self.est_publie and not self.date_publication:
            from django.core.exceptions import ValidationError
            raise ValidationError({
                "date_publication": "Un article publié doit obligatoirement avoir une date de publication."
            })
