import re
from django.apps import apps
from django.db import models
from apps.core.app_main.models.tags import Tag

# =====================================================================
# 📂 STOCKAGE DES PATTERNS D'URLS POUR LE NOMMAGE DES PAGES DYNAMIQUES
# =====================================================================

class DynamicPagePattern(models.Model):
    category = models.CharField(max_length=50, unique=True, verbose_name="Catégorie")
    pattern = models.CharField(max_length=255, verbose_name="Pattern d'URL")
    display_format = models.CharField(
        max_length=255, 
        verbose_name="Format d'affichage",
        help_text="Utilisez {name} pour insérer le vrai nom. Exemple: '{name} / Discographie'"
    )
    real_name_field = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Champ du vrai nom",
        help_text="Exemple: 'Artiste.name' pour récupérer le vrai nom de l'artiste"
    )

    class Meta:
        ordering = ["category"]
        verbose_name = "Pattern de page dynamique"
        verbose_name_plural = "Pages dynamiques - URLS"

    def __str__(self):
        return f"{self.category} → {self.display_format}"
    
# ===========================================================
# 📂 NOMMAGE AUTOMATIQUE DES PAGES DYNAMIQUES DES AUTRES APP
# ===========================================================

def generate_display_name(self):
    """Génère un display_name basé sur les patterns stockés en base"""

    # Pages dynamiques d'app_main (cas à part car pas d'ID dans l'URL)
    APP_MAIN_PAGES = {
        "telechargements": "Téléchargements",
        "index": "Index",
        "tags": "Tags",
        # ➕ Ajoute ici d'autres pages dynamiques non structurées
    }
    
    if self.page_name in APP_MAIN_PAGES:
        return APP_MAIN_PAGES[self.page_name]  # Nom fixe pour app_main

    # Récupérer le vrai nom (s'il existe)
    real_name = self.get_real_name()

    # Vérifier si un pattern existe en base
    from app_main.models import DynamicPagePattern  
    for pattern in DynamicPagePattern.objects.all():
        if self.page_name.startswith(pattern.pattern.split("/{}/")[0]):
            return pattern.display_format.format(name=real_name)

    # Cas général si aucun pattern ne correspond
    return real_name

# ================================
# 📂 NOMMAGE DES PAGES DYNAMIQUES
# ================================

class DynamicPageInfo(models.Model):
    page_name = models.CharField(max_length=255, unique=True, verbose_name="Nom technique")
    display_name = models.CharField(
        max_length=255, verbose_name="Nom affiché", blank=True, null=True
    )

    class Meta:
        ordering = ["display_name"]
        verbose_name = "Nom de page dynamique"
        verbose_name_plural = "Pages dynamiques - Noms"
        indexes = [
            models.Index(fields=["page_name"]),  # 🔹 Accélère les recherches par nom technique
        ]
    
    def get_real_name(self):
        """Récupère le vrai nom depuis la base de données en utilisant `real_name_field`."""
        if not self.page_name:
            return None

        try:
            # Vérifier si un pattern correspondant existe
            pattern = DynamicPagePattern.objects.filter(pattern__startswith=self.page_name.split("/")[0]).first()
            if not pattern or not pattern.real_name_field:
                return self.page_name.replace("-", " ").title()

            # Extraire le modèle et le champ
            model_name, field_name = pattern.real_name_field.split(".")
            model = apps.get_model("app_main", model_name)

            # Extraire l'ID à partir du `page_name`
            match = re.match(r"(\d+)-([\w-]+)", self.page_name)
            if match:
                entity_id = match.group(1)
                obj = model.objects.filter(id=entity_id).only(field_name).first()
                return getattr(obj, field_name, None) if obj else None

        except Exception as e:
            print(f"⚠️ Erreur récupération vrai nom pour {self.page_name} : {e}")

        return self.page_name.replace("-", " ").title()

    def generate_display_name(self):
        """Génère un nom affiché à partir de `page_name`, avec correction automatique."""
        real_name = self.get_real_name()
        if real_name:
            name = real_name  # Utilise directement le vrai nom s'il existe
        else:
            name = self.page_name.replace("-", " ").title()  # Ex: "best-of" → "Best Of"

        # 🔹 Corrige tous les cas où "dj" ou "mc" sont des mots isolés
        name = re.sub(r'\b[dD][jJ]\b', 'DJ', name)  # Corrige "dj", "Dj", "dJ", "DJ"
        name = re.sub(r'\b[mM][cC]\b', 'MC', name)  # Corrige "mc", "Mc", "mC", "MC"

        return name

    def save(self, *args, **kwargs):
        """Si `display_name` est vide, on le génère automatiquement."""
        if not self.display_name:
            self.display_name = self.generate_display_name() # Utilise le vrai nom si dispo
        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name or self.page_name

# ====================================
# 📂 TAGS POUR LES PAGES DYNAMIQUES
# ====================================

class DynamicPageTag(models.Model):
    """
    Associe un tag à une page dynamique.
    """
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="dynamic_pages")
    page_name = models.CharField(max_length=255, verbose_name="Nom de la page dynamique")
    display_name = models.CharField(max_length=255, verbose_name="Nom affiché", blank=True, null=True)  # ← Vérifie si un champ similaire existe
    page_info = models.ForeignKey(
        DynamicPageInfo, on_delete=models.CASCADE, related_name="tags", null=True, blank=True
    )
    
    class Meta:
        ordering = ["page_name"]
        verbose_name = "Tag de page dynamique"
        verbose_name_plural = "Pages dynamiques - Tags"
        indexes = [
            models.Index(fields=["page_name"]),  # 🔹 Accélère la recherche par page
            models.Index(fields=["tag"]),  # 🔹 Accélère les recherches par tag
        ]

    def __str__(self):
        return f"{self.tag.name} → {self.display_name or self.page_name}"
