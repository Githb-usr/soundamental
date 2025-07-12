from django.contrib import admin  # 🔹 Import obligatoire pour personnaliser l'admin

from .static_pages import StaticPageMetaAdmin, StaticPageHistoryAdmin, StaticPageHistoryInline
from .downloads import DownloadableFileAdmin, DownloadLogAdmin
from .tags import TagAdmin
from .dynamic_pages import DynamicPageInfoAdmin, DynamicPagePatternAdmin, DynamicPageTagAdmin
from apps.core.app_main.models.settings import AppMainSettings

##=======================================
## Personnalisation de l'interface Admin
##=======================================
admin.site.site_header = "Administration de Soundamental.fr"
admin.site.site_title = "Soundamental Admin"
admin.site.index_title = "Gestion du site"

@admin.register(AppMainSettings)
class AppMainSettingsAdmin(admin.ModelAdmin):
    list_display = ("name", "value")
    search_fields = ("name",)
