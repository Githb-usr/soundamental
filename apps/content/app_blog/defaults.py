from django.conf import settings

# --- Blog : configuration des images ---
# Si le projet a défini cette valeur dans ses settings, on la prend.
# Sinon, on applique un fallback (1200 / 85 ici).
BLOG_IMAGE_MAX_WIDTH = getattr(settings, "BLOG_IMAGE_MAX_WIDTH", 1200)
BLOG_IMAGE_JPEG_QUALITY = getattr(settings, "BLOG_IMAGE_JPEG_QUALITY", 85)
