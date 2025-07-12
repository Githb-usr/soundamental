from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from apps.core.app_index.models import IndexEntry, IndexSettings, PageExistence
from django.conf import settings

# Définition de la ressource pour gérer l'import/export des entrées de l'index
class IndexEntryResource(resources.ModelResource):
    class Meta:
        model = IndexEntry  # On lie cette ressource au modèle IndexEntry
        fields = ("name", "category", "id_forum")  # Champs à importer/exporter
        import_id_fields = ("name",)  # Le champ "name" sert d'identifiant unique

    def before_import_row(self, row, **kwargs):
        """
        Avant l'import de chaque ligne :
        - Nettoie les champs.
        - Vérifie si l'entrée existe.
        - Met à jour `id_forum` uniquement si nécessaire.
        """
        try:
            name = row.get("name", "").strip()
            category = row.get("category", "").strip()
            id_forum = row.get("id_forum", "").strip() or None  # Remplace "" par None

            if not name or not category:
                print(f"⚠️ Ligne ignorée : Nom ou catégorie manquant ({row})")
                return  # Ignore les lignes invalides

            # Vérifie si l'entrée existe déjà
            entry = IndexEntry.objects.filter(name=name).first()

            if entry:
                if id_forum and entry.id_forum != id_forum:  # 🔹 Met à jour uniquement si nécessaire
                    entry.id_forum = id_forum
                    entry.save()
            else:
                IndexEntry.objects.create(name=name, category=category, id_forum=id_forum)

        except Exception as e:
            print(f"❌ Erreur lors de l'import d'une ligne : {e}")

# Configuration de l'admin Django pour IndexEntry
class IndexEntryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
    Ajoute la gestion des imports et exports Excel dans l'admin Django.
    - Permet d'importer des entrées en masse.
    - Affiche les champs utiles pour une gestion facile.
    """
    resource_class = IndexEntryResource  # Associe la ressource d'import/export
    list_display = ("name", "category", "liens_existant", "id_forum")  # Colonnes affichées dans la liste admin
    search_fields = ("name", "category", "id_forum")  # Ajoute la recherche
    list_filter = ("category",)  # Ajoute un filtre par catégorie
    
    # Conserve tous les formats d'importation et ajoute Excel
    def get_import_formats(self):
        formats = super().get_import_formats()
        # formats.append(base_formats.XLSX)
        return formats
    
    def save_model(self, request, obj, form, change):
        obj.save()  # Laisse Django gérer l'INSERT ou UPDATE normalement
        # 🔹 Force l'enregistrement en base
        super().save_model(request, obj, form, change)
    
    def liens_existant(self, obj):
        codes = settings.INDEX_LINK_CODES  # Ex: {"biography": "BIO", "discography": "DIS", ...}
        template = settings.INDEX_LINK_TEMPLATES.get(obj.category.lower(), [None] * 5)

        liens = obj.get_links
        visibles = []

        for key, link in zip(template, liens):
            if key and link:
                visibles.append(codes.get(key, key.upper()))

        return ", ".join(visibles)

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
        print(f"📌 Enregistrement dans PageExistence : {obj.category} - {obj.name} - {obj.page_type}")  # Debug console
        obj.save()
        super().save_model(request, obj, form, change)
