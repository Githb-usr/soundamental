from django.contrib import admin
from apps.core.app_main.models.dynamic_pages import DynamicPageInfo, DynamicPagePattern, DynamicPageTag

# ========================================
# 📂 GESTION DES NOMS DE PAGES DYNAMIQUES
# ========================================

@admin.register(DynamicPageInfo)
class DynamicPageInfoAdmin(admin.ModelAdmin):
    list_display = ("page_name", "generated_display_name")  # Affichage en liste
    search_fields = ("page_name", "display_name")  # Barre de recherche
    
    def get_model_perms(self, request):
        """
        Personnalise l'affichage de la section dans l'admin.
        """
        perms = super().get_model_perms(request)
        perms["view"] = True  # Assure que la section est visible
        return perms
    
    def generated_display_name(self, obj):
        return obj.generate_display_name()  # Utilise la fonction de correction

    generated_display_name.short_description = "Nom affiché"

@admin.register(DynamicPagePattern)
class DynamicPagePatternAdmin(admin.ModelAdmin):
    list_display = ("category", "pattern", "display_format", "real_name_field")
    search_fields = ("category", "pattern", "display_format", "real_name_field")

@admin.register(DynamicPageTag)
class DynamicPageTagAdmin(admin.ModelAdmin):
    """
    Admin pour la gestion des tags associés aux pages dynamiques.
    Permet d'éviter les erreurs en facilitant la sélection des pages dynamiques.
    """
    list_display = ("tag", "page_name", "display_name", "page_info_display")  # Affichage dans la liste admin
    search_fields = ("tag__name", "page_name", "display_name")  # Barre de recherche sur ces champs
    autocomplete_fields = ("tag",)  # Active la recherche des tags
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Remplace la saisie manuelle de `page_info` par une liste déroulante
        contenant toutes les pages dynamiques enregistrées dans DynamicPageInfo.
        """
        if db_field.name == "page_info":
            kwargs["queryset"] = DynamicPageInfo.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """
        Ajoute des descriptions sous chaque champ pour guider l'utilisateur.
        """
        help_texts = {
            "page_name": "Entrez le nom technique de la page dynamique (ex: 'artistes/5687-michael-jackson').",
            "display_name": "Optionnel : Nom affiché dans l'interface. Si vide, il sera généré automatiquement.",
            "page_info": "Associe ce tag à une page dynamique existante dans DynamicPageInfo. Laisser vide si la page n'existe pas encore.",
        }
        if db_field.name in help_texts:
            kwargs["help_text"] = help_texts[db_field.name]  # Ajoute l'aide contextuelle
        return super().formfield_for_dbfield(db_field, request, **kwargs)
    
    def page_info_display(self, obj):
        return obj.page_info.display_name if obj.page_info else "—"

    page_info_display.short_description = "Page dynamique"  # Renomme la colonne

