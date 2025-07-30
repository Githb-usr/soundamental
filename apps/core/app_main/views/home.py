import random
from django.shortcuts import render

def home_view(request):
    """
    Vue pour la page d'accueil avec carrousel d'images aléatoires par groupes de 3.
    """

    # Pool d'images carrées (chemins relatifs ou absolus depuis static ou media)
    image_pool = [
        "/media/site/illustrations/carrousel/carrousel01.jpg",
        "/media/site/illustrations/carrousel/carrousel02.jpg",
        "/media/site/illustrations/carrousel/carrousel03.jpg",
        "/media/site/illustrations/carrousel/carrousel04.jpg",
        "/media/site/illustrations/carrousel/carrousel05.jpg",
        "/media/site/illustrations/carrousel/carrousel06.jpg",
        "/media/site/illustrations/carrousel/carrousel07.jpg",
        "/media/site/illustrations/carrousel/carrousel08.jpg",
        "/media/site/illustrations/carrousel/carrousel09.jpg",
        "/media/site/illustrations/carrousel/carrousel10.jpg",
        "/media/site/illustrations/carrousel/carrousel11.jpg",
        "/media/site/illustrations/carrousel/carrousel12.jpg",
        # ...ajoute tous tes fichiers ici...
    ]

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
