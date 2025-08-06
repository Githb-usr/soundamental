# apps/content/app_blog/admin.py

from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Article, CategorieArticle
from .forms.admin_forms import ArticleAdminForm


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('titre', 'categorie_principale', 'get_categories_secondaires','est_publie', 'date_publication', 'auteur', 'image_preview', 'views', 'last_viewed')
    list_filter = ('est_publie', 'date_publication')
    search_fields = ('titre', 'resume', 'contenu', 'auteur__username')
    prepopulated_fields = {'slug': ('titre',)}
    ordering = ['-date_publication']
    readonly_fields = ('image_preview', 'date_modification')
    autocomplete_fields = ['tags', 'categorie_principale', 'categories_secondaires']

    fieldsets = (
        (None, {
            'fields': (
                'titre', 'slug', 'auteur', 'categorie_principale', 'categories_secondaires',
                'resume', 'contenu', 'image', 'masquer_image', 'image_preview', 'est_publie', 'tags'
            )
        }),
        ('Dates (automatiques)', {
            'fields': ('date_publication', 'date_modification'),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" style="border-radius:5px;" />')
        return "(Aucune image)"
    image_preview.short_description = "Aperçu"
    image_preview.admin_order_field = 'image'
    
    def get_categories_secondaires(self, obj):
        return ", ".join([c.nom for c in obj.categories_secondaires.all()])
    get_categories_secondaires.short_description = "Catégories secondaires"
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Affiche un message si l’image a été modifiée par le modèle
        if hasattr(obj, "_image_traitement_info"):
            messages.info(request, obj._image_traitement_info)


    class Media:
        js = [
            "js/tinymce/tinymce.min.js",
            "js/tinymce_rich_init.js",
        ]
        

@admin.register(CategorieArticle)
class CategorieArticleAdmin(admin.ModelAdmin):
    list_display = ('id','nom', 'slug', 'description')
    search_fields = ('nom', 'slug', 'description')
    ordering = ['nom']
    fields = ('nom', 'slug', 'description')  # ← ordre affiché dans le formulaire
    prepopulated_fields = {'slug': ('nom',)}
