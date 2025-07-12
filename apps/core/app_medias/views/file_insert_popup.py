from pathlib import Path
from collections import OrderedDict

from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_GET


@require_GET
@login_required
@user_passes_test(lambda u: u.is_staff or u.has_perm("app_blog.add_article"))
def media_images_insert_view(request):
    """
    Vue pour insérer une image existante dans TinyMCE via une popup.

    - Affiche tous les dossiers principaux même vides
    - Affiche les sous-dossiers uniquement s’ils contiennent des images
    - Indique si une entrée est un sous-dossier (champ : sous_dossier_de)
    """
    bibliotheques = getattr(settings, "IMAGES_BIBLIOTHEQUES", {})
    images_par_dossier = OrderedDict()

    for key, config in bibliotheques.items():
        racine = Path(settings.MEDIA_ROOT) / config["path"]
        rel_url = settings.MEDIA_URL + config["path"].rstrip("/") + "/"
        label_base = config["label"]

        # Ajout du dossier principal
        images_par_dossier[key] = {
            "label": label_base,
            "fichiers": [],
            "sous_dossier_de": None,
        }

        if not racine.exists():
            continue

        # Images directement dans le dossier principal
        fichiers_racine = sorted([
            {
                "url": f"{rel_url}{f.name}",
                "nom": f.name,
            }
            for f in racine.iterdir()
            if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif", ".webp"]
        ], key=lambda x: x["nom"])

        images_par_dossier[key]["fichiers"] = fichiers_racine

        # Parcours des sous-dossiers
        for element in sorted(racine.iterdir()):
            if not element.is_dir():
                continue

            fichiers = sorted([
                {
                    "url": f"{rel_url}{element.name}/{f.name}",
                    "nom": f.name,
                }
                for f in element.iterdir()
                if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png", ".gif", ".webp"]
            ], key=lambda x: x["nom"])

            if fichiers:
                images_par_dossier[f"{key}::{element.name}"] = {
                    "label": element.name.replace('_', ' ').capitalize(),
                    "fichiers": fichiers,
                    "sous_dossier_de": key,
                }

    dossier_selectionne = request.GET.get("dossier")
    if not dossier_selectionne or dossier_selectionne not in images_par_dossier:
        dossier_selectionne = next(iter(images_par_dossier), None)

    return render(request, "app_medias/image_insert_popup.html", {
        "images_par_dossier": images_par_dossier,
        "dossier_selectionne": dossier_selectionne,
    })
