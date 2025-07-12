from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.forms import Textarea
from django.urls import reverse
from apps.core.app_main.forms.static_pages import StaticPageForm
from apps.core.app_main.models.static_pages import StaticPageHistory, StaticPageMeta


class StaticPageHistoryInline(admin.TabularInline):
    """
    Affichage de l'historique des modifications dans l'admin.
    """
    model = StaticPageHistory
    extra = 0
    can_delete = False
    fields = ("modified_at", "modified_by", "admin_link")
    readonly_fields = ("modified_at", "modified_by", "admin_link")
    
    def admin_link(self, obj):
        if obj.pk:
            url = reverse('admin:app_main_staticpagehistory_change', args=[obj.pk])
            return format_html('<a href="{}">Gérer</a>', url)
        return "-"

    admin_link.short_description = "Modifier/Supprimer"
    
@admin.register(StaticPageHistory)
class StaticPageHistoryAdmin(admin.ModelAdmin):
    """
    Admin pour l'historique des modifications des pages statiques.
    Lecture seule.
    """
    list_display = ("page", "modified_at", "modified_by")
    search_fields = ("page__title",)
    list_filter = ("modified_at",)
    ordering = ("-modified_at",)
    readonly_fields = ("page", "modified_at", "modified_by")
    
    def has_delete_permission(self, request, obj=None):
        """Empêche la suppression des entrées de l'historique."""
        return request.user.is_superuser

    def has_add_permission(self, request):
        """Empêche l'ajout manuel d'entrées dans l'historique."""
        return False


@admin.register(StaticPageMeta)
class StaticPageMetaAdmin(admin.ModelAdmin):
    """
    Admin des pages statiques avec suivi des modifications.
    """
    list_display = ("title", "slug", "category", "published", "created_at", "updated_at")
    search_fields = ("title", "slug", "content")
    list_filter = ("category", "published", "created_at", "updated_at")
    ordering = ("title",)
    autocomplete_fields = ("tags",)  # Active la recherche pour sélectionner un tag facilement
    inlines = [StaticPageHistoryInline]  # Ajout de l'historique dans l'admin
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
    prepopulated_fields = {"slug": ("title",)}
    form = StaticPageForm

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si c'est une création
            obj.created_by = request.user
        obj.updated_by = request.user  # Toujours mis à jour
        super().save_model(request, obj, form, change)

        # Avertissement si on a mis des tags sur la page "aide"
        if obj.slug == "aide" and obj.tags.exists():
            self.message_user(
                request,
                "⚠️ Les tags ne sont pas utilisés sur la page 'aide'. Vous pouvez les retirer.",
                level="warning"
            )