from django.conf import settings
from django.shortcuts import render
import os
import random

def home_view(request):
    """
    Vue pour la page d'accueil avec carrousel d'images aléatoires par groupes de 4.
    - On charge automatiquement toutes les images du dossier media dédié.
    - On mélange deux fois la liste pour limiter les séquences logiques.
    - On limite le nombre d'images envoyées au template (perf/DOM).
    - On découpe en slides de 4 images. (La 4e sera masquée en <768px au niveau CSS.)
    """

    # =========================
    # Paramètres de présentation
    # =========================
    NB_SLIDES = 3                 # Nombre de slides rendus (ajuste si besoin)
    IMAGES_PER_SLIDE = 4          # 4 en desktop/tablette ; en mobile on masquera la 4e via CSS
    MAX_IMAGES = NB_SLIDES * IMAGES_PER_SLIDE

    # ==========================================
    # Chargement des images depuis MEDIA_ROOT
    # Dossier fixe : /media/site/illustrations/carrousel/
    # ==========================================
    folder = os.path.join(settings.MEDIA_ROOT, "site", "illustrations", "carrousel")
    image_pool = []

    # Vérifie l'existence du dossier ; si absent, on renvoie un carrousel vide (aucune erreur levée)
    if os.path.isdir(folder):
        try:
            # On ne retient que les fichiers image usuels
            valid_ext = (".jpg", ".jpeg", ".png", ".webp")
            for filename in os.listdir(folder):
                if filename.lower().endswith(valid_ext):
                    # Chemin web utilisable dans le template (MEDIA_URL + sous-chemin)
                    image_pool.append(
                        f"{settings.MEDIA_URL.rstrip('/')}/site/illustrations/carrousel/{filename}"
                    )
        except OSError:
            # Cas rare : problème d'I/O → on laisse image_pool vide (fallback propre)
            image_pool = []

    # =========================
    # Mélange aléatoire robuste
    # =========================
    temp = image_pool.copy()
    random.shuffle(temp)
    random.shuffle(temp)

    # ==========================================
    # Sélection d'un nombre limité d'images (perf)
    # ==========================================
    if MAX_IMAGES > 0:
        images = temp[:min(MAX_IMAGES, len(temp))]
    else:
        images = temp

    # ===========================
    # Découpage en slides de 4
    # (le template itérera sur ces slides)
    # ===========================
    slides = [images[i:i + IMAGES_PER_SLIDE] for i in range(0, len(images), IMAGES_PER_SLIDE)]

    # ======================================================
    # Contexte envoyé au template
    # - carousel_slides : liste de listes (4 images/slide)
    # - slide_count     : nombre réel de slides (pour indicateurs dynamiques)
    # - images_per_slide: valeur 4 (info utile au besoin côté template/CSS)
    # ======================================================
    context = {
        "carousel_slides": slides,
        "slide_count": len(slides),
        "images_per_slide": IMAGES_PER_SLIDE,
        # ... autres variables de contexte si besoin ...
    }

    return render(request, "pages/home.html", context)
