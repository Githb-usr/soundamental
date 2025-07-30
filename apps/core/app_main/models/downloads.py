import os
from datetime import date
from django.db import models
from django.db.models import F
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.conf import settings

# ====================================
# 📂 MODÈLES POUR LES TÉLÉCHARGEMENTS
# ====================================

def generate_versioned_filename(base_dir, original_name, ext):
    """
    Crée un nom de fichier semi-lisible et versionné : 
    nom-de-base_2025-05-08_v01.pdf
    """
    name_slug = slugify(original_name)[:50]
    today = date.today().isoformat()
    version = 1

    # Nom sans suffixe
    candidate = f"{name_slug}{ext.lower()}"
    full_path = os.path.join(base_dir, candidate)
    if not os.path.exists(full_path):
        return candidate

    # Nom avec date
    candidate = f"{name_slug}_{today}{ext.lower()}"
    full_path = os.path.join(base_dir, candidate)
    if not os.path.exists(full_path):
        return candidate

    # Boucle versionnée
    while True:
        candidate = f"{name_slug}_{today}_v{version:02d}{ext.lower()}"
        full_path = os.path.join(base_dir, candidate)
        if not os.path.exists(full_path):
            return candidate
        version += 1

def upload_to(instance, filename):
    """Définit le chemin de stockage du fichier téléchargeable."""
    name, ext = os.path.splitext(filename)
    base_dir = os.path.join("downloads", "data")
    final_name = generate_versioned_filename(os.path.join(settings.MEDIA_ROOT, base_dir), name, ext)
    return os.path.join(base_dir, final_name)

def upload_image(instance, filename):
    """Définit le chemin de stockage des images associées au fichier."""
    name, ext = os.path.splitext(filename)
    base_dir = os.path.join("downloads", "images")
    final_name = generate_versioned_filename(os.path.join(settings.MEDIA_ROOT, base_dir), name, ext)
    return os.path.join(base_dir, final_name)

class DownloadableFile(models.Model):
    """
    Modèle pour gérer les fichiers téléchargeables.
    """
    title = models.CharField(max_length=255, verbose_name="Nom du fichier")
    subtitle = models.CharField(
        max_length=255,
        blank=True,
        help_text="Sous-titre optionnel affiché sous le titre principal."
    )
    description = models.TextField(blank=True, verbose_name="Description")
    
    file = models.FileField(
        upload_to=upload_to,
        verbose_name="Fichier",
        validators=[FileExtensionValidator(allowed_extensions=["csv", "docx", "jpg", "mp3", "pdf", "png", "xlsx", "zip"])],
    )

    image = models.ImageField(
        upload_to=upload_image,
        verbose_name="Image",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["gif", "jpg", "png"])],
    )
    
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    download_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de téléchargements")

    def get_file_size(self):
        """Renvoie la taille du fichier en octets (ou 0 si manquant)."""
        if self.file and hasattr(self.file, "path") and os.path.exists(self.file.path):
            return self.file.size
        return 0

    class Meta:
        unique_together = ("title", "subtitle")  # Contraintes d’unicité sur le couple
        ordering = ["-uploaded_at"]
        verbose_name = "Fichier téléchargeable"
        verbose_name_plural = "Téléchargements - Fichiers"
        indexes = [
            models.Index(fields=["download_count"]),
        ]

    def register_download(self):
        """Incrémente le compteur de téléchargements + log."""
        DownloadableFile.objects.filter(id=self.id).update(download_count=F("download_count") + 1)
        DownloadLog.objects.create(file=self)

    def __str__(self):
        return self.title

class DownloadLog(models.Model):
    """
    Modèle pour enregistrer chaque téléchargement avec sa date.
    """
    file = models.ForeignKey(DownloadableFile, on_delete=models.CASCADE, related_name="logs")
    downloaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Date du téléchargement")

    class Meta:
        ordering = ["-downloaded_at"]
        verbose_name = "Historique des téléchargements"
        verbose_name_plural = "Téléchargements - Historiques"

    def __str__(self):
        return f"{self.file.title} téléchargé le {self.downloaded_at.strftime('%Y-%m-%d %H:%M:%S')}"
