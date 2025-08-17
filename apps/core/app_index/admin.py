from django import forms
from django.db import transaction
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from django.conf import settings
import logging

# Import via l’agrégateur de l’app (inclut désormais IndexAlias)
from apps.core.app_index.models import IndexEntry, IndexSettings, PageExistence, Category, PageType, IndexAlias


# =========================
# Journalisation import index
# =========================

# Initialisation du logger (placé tout en haut du fichier si pas déjà fait)
logger = logging.getLogger("import_index")
handler = logging.FileHandler("logs/import_index.log", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# =========================
# Ressource import/export
# =========================

# Définition de la ressource pour gérer l'import/export des entrées de l'index
class IndexEntryResource(resources.ModelResource):
    category = Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(Category, field="code")
    )

    class Meta:
        model = IndexEntry  # On lie cette ressource au modèle IndexEntry
        fields = ("name", "category", "id_forum")  # Champs à importer/exporter
        import_id_fields = ("name",)  # Le champ "name" sert d'identifiant unique

    def before_import_row(self, row, **kwargs):
        """
        Avant l'import de chaque ligne :
        - Nettoie les données.
        - Vérifie si une entrée existe.
        - Met à jour `id_forum` si nécessaire.
        - Affiche et enregistre un message clair pour chaque cas.
        """
        name = row.get("name", "").strip()
        category_code = row.get("category", "").strip()
        id_forum = row.get("id_forum", "").strip() or None

        if not name or not category_code:
            msg = f"⚠️ Ignoré (champ manquant) → name: '{name}' / category: '{category_code}'"
            print(msg)
            logger.warning(msg)
            return

        category = Category.objects.filter(code=category_code).first()
        if not category:
            msg = f"❌ Catégorie inconnue : {category_code}"
            print(msg)
            logger.error(msg)
            return

        row["category"] = category.code  # Injection directe

        entry = IndexEntry.objects.filter(name=name).first()

        if entry:
            if id_forum and entry.id_forum != id_forum:
                msg = f"✏️ Mise à jour : {name} → id_forum modifié"
                entry.id_forum = id_forum
                entry.save()
            else:
                msg = f"🔁 Doublon (inchangé) : {name}"
            print(msg)
            logger.info(msg)
        else:
            msg = f"➕ Nouvelle entrée : {name}"
            print(msg)
            logger.info(msg)
            # La création est laissée à import_export (pas de .create ici)

# =========================
# Inline pour les alias
# =========================
class IndexAliasInline(admin.TabularInline):
    """
    Inline pour gérer les alias directement depuis la fiche d'une entrée.
    - La catégorie et 'alias_normalized' sont gérés automatiquement côté modèle.
    """
    model = IndexAlias
    extra = 1
    fields = ("alias", "is_listed")
    verbose_name = "Alias / variation"
    verbose_name_plural = "Alias / variations"


# =========================
# Admin IndexEntry
# =========================

# Configuration de l'admin Django pour IndexEntry
class IndexEntryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    Ajoute la gestion des imports et exports Excel dans l'admin Django.
    - Permet d'importer des entrées en masse.
    - Affiche les champs utiles pour une gestion facile.
    """
    resource_class = IndexEntryResource  # Associe la ressource d'import/export
    list_display = ("name", "category", "liens_existant", "id_forum")  # Colonnes affichées dans la liste admin
    search_fields = ("name", "category__code", "id_forum")  # Ajoute la recherche
    list_filter = ("category",)  # Ajoute un filtre par catégorie
    
    inlines = [IndexAliasInline]

    # Conserve tous les formats d'importation et ajoute Excel
    def get_import_formats(self):
        formats = super().get_import_formats()
        # formats.append(base_formats.XLSX)
        return formats

    def save_model(self, request, obj, form, change):
        # Force l'enregistrement en base
        super().save_model(request, obj, form, change)

    def liens_existant(self, obj):
        codes = settings.INDEX_LINK_CODES  # Ex: {"biography": "BIO", "discography": "DIS", ...}
        template = settings.INDEX_LINK_TEMPLATES.get(obj.category.code, [None] * 5)
        liens = obj.get_links   
        visibles = []
        for key, link in zip(template, liens):
            if key and isinstance(link, str):
                visibles.append(codes.get(key, key.upper()))

        return ", ".join(visibles)
    
    # Rend l'enregistrement de la fiche + inlines atomique : tout passe ou rien
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if request.method == "POST":
            with transaction.atomic():
                return super().changeform_view(request, object_id, form_url, extra_context)
        return super().changeform_view(request, object_id, form_url, extra_context)


# Enregistre IndexEntry dans l'admin
admin.site.register(IndexEntry, IndexEntryAdmin)

##====================================================
## Gestion de l'affichage des sous-lettres de l'index
##====================================================
@admin.register(IndexSettings)
class IndexSettingsAdmin(admin.ModelAdmin):
    list_display = ("category", "apply_to_all", "letters_with_sub_buttons")
    search_fields = ("category",)
    fields = ("category", "apply_to_all", "letters_with_sub_buttons")

    def save_model(self, request, obj, form, change):
        """
        Force la mise à jour de `letters_with_sub_buttons` quand `apply_to_all` est coché.
        """
        if obj.apply_to_all:
            obj.letters_with_sub_buttons = "0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,@"
        super().save_model(request, obj, form, change)

# =========================
# Admin PageExistence
# =========================

@admin.register(PageExistence)
class PageExistenceAdmin(admin.ModelAdmin):
    """
    Interface d'administration pour gérer les pages existantes.

    - Permet de voir quelles pages existent déjà.
    - Possibilité d'ajouter/supprimer des entrées manuellement si nécessaire.
    - Filtres pour afficher les pages par catégorie et par type.
    - Recherche possible par nom d'entrée.
    """

    list_display = ("category", "name", "page_type")  # 🔹 Affichage dans l'admin
    list_filter = ("category", "page_type")  # 🔹 Filtres pour trier rapidement
    search_fields = ("name",)  # 🔹 Recherche par nom d'entrée
    list_per_page = 50  # 🔹 Définit le nombre d'entrées affichées par page

    def save_model(self, request, obj, form, change):
        obj.save()
        super().save_model(request, obj, form, change)

# =========================
# Admin Category
# =========================

# Ajout des configurations pour les nouvelles tables Category et PageType
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "label", "description")
    search_fields = ("code", "name", "label", "description")
    fields = ("code", "name", "label", "description")
    ordering = ("name",)
    
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['code'].help_text += (
            "<br><br><span style='color: red;'>"
            "⚠️ Toute nouvelle catégorie doit être ajoutée dans les constantes "
            "<b>INDEX_LINK_TEMPLATES</b> (obligatoire) et <b>CATEGORY_MAPPING</b> (si la catégorie doit apparaître dans l’index principal) du fichier "
            "<b>config/settings/project.py</b> !</span>"
        )
        return super().render_change_form(request, context, *args, **kwargs)

# =========================
# Admin PageType
# =========================

@admin.register(PageType)
class PageTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "label", "description")
    search_fields = ("code", "label", "description")
    ordering = ("code", "label")

# =========================
# Admin IndexAlias 
# =========================
class IndexAliasResource(resources.ModelResource):
    """
    Ressource d'import/export des alias.
    - 'entry' est résolu par le NOM de l'IndexEntry (plus simple que l'ID).
    - 'category' et 'alias_normalized' sont calculés automatiquement en save().
    """
    entry = Field(
        column_name="entry",                 # colonne CSV
        attribute="entry",                   # champ du modèle
        widget=ForeignKeyWidget(IndexEntry, field="name")  # lookup par nom
    )

    class Meta:
        model = IndexAlias
        fields = ("entry", "alias", "is_listed")
        import_id_fields = ("entry", "alias")  # permet la mise à jour si même couple

@admin.register(IndexAlias)
class IndexAliasAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    import_template_name = "admin/app_index/indexalias/import.html"
    resource_class = IndexAliasResource
    list_display = ("alias", "entry", "category", "is_listed")
    list_filter = ("category", "is_listed")
    search_fields = ("alias", "entry__name")
