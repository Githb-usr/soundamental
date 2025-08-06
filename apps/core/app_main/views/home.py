from django.conf import settings
import os
import random
from django.shortcuts import render

def home_view(request):
    """
    Vue pour la page d'accueil avec carrousel d'images aléatoires par groupes de 3.
    """

    # Pool d'images carrées (chemins relatifs ou absolus depuis static ou media)
    # => Correction : chargement automatique de tous les fichiers du dossier cible
    folder = os.path.join(settings.MEDIA_ROOT, "site", "illustrations", "carrousel")
    image_pool = []
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # On prépare le chemin relatif attendu par le template (media)
            image_pool.append(f"/media/site/illustrations/carrousel/{filename}")

    # Mélange deux fois la liste pour casser les séquences logiques
    temp = image_pool.copy()
    random.shuffle(temp)
    random.shuffle(temp)

    nb_images = 9  # 3 slides de 3 images chacune
    images = temp[:min(nb_images, len(temp))]

    # Découpe en groupes de 3 images pour chaque slide
    slides = [images[i:i+3] for i in range(0, len(images), 3)]

    context = {
        "carousel_slides": slides,
        # ... ajoute ici d'autres variables pour le template si besoin ...
    }

    return render(request, "pages/home.html", context)
