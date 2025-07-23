from django.contrib import admin
from apps.core.app_main.models.tags import Tag
from apps.core.app_main.models.tag_meta import TagPageMeta

# =================
# 📂 AJOUT DE TAGS
# =================

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "category", "description", "access_level")  # Affichage des colonnes principales
    prepopulated_fields = {"slug": ("name",)}
    fields = ("name", "slug", "category", "description", "access_level")
    search_fields = ("name", "category__name")  # Recherche par nom + sur le nom de la catégorie
    
    def has_delete_permission(self, request, obj=None):
        """Empêche la suppression des tags système."""
        if obj and obj.name.lower() in ["artiste", "compilation", "label", "lexique"]:
            return False
        return super().has_delete_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        """Verrouille le slug UNIQUEMENT pour les tags système."""
        protected_tags = ["artiste", "compilation", "label", "lexique"]
        
        if obj and obj.name.lower() in protected_tags:
            return self.readonly_fields + ("slug",)  # 🔹 Slug bloqué pour les tags système

        return self.readonly_fields  # 🔹 Sinon, slug modifiable

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """
        Ajoute un message d'avertissement si le champ `slug` est modifié.
        """
        if db_field.name == "slug":
            kwargs["help_text"] = "⚠️ Modifier le slug peut casser des liens existants."
        
        return super().formfield_for_dbfield(db_field, request, **kwargs)

@admin.register(TagPageMeta)
class TagPageMetaAdmin(admin.ModelAdmin):
    list_display = ["tag", "get_related_tags"]
    filter_horizontal = ["related_tags"]

    def get_related_tags(self, obj):
        return ", ".join([t.name for t in obj.related_tags.all()])
    get_related_tags.short_description = "Tags associés"
