import os
import hashlib
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.files.uploadedfile import UploadedFile
from django.utils.text import slugify

@csrf_exempt
@require_POST
@login_required
def upload_image_blog(request):
    """
    Upload d’image pour les articles de blog (TinyMCE).
    Trie par catégorie (si fournie), évite les doublons, génère un nom propre et unique.
    """
    if not request.META.get("HTTP_X_CSRFTOKEN"):
        return HttpResponseForbidden("CSRF token manquant.")

    image: UploadedFile = request.FILES.get("image")
    if not image:
        return HttpResponseBadRequest("Aucun fichier envoyé.")

    category = request.POST.get("category", "autres")  # Ex : "news_artistes"
    base_dir = os.path.join(settings.MEDIA_ROOT, "images", "blog", slugify(category))
    base_url = os.path.join(settings.MEDIA_URL, "images", "blog", slugify(category))

    os.makedirs(base_dir, exist_ok=True)

    # Hash du contenu
    content_hash = hashlib.md5(image.read()).hexdigest()
    image.seek(0)

    name, ext = os.path.splitext(image.name)
    base_name = slugify(name) or "image"
    index = 1

    # Boucle pour générer un nom unique
    while True:
        filename = f"{base_name}_{index:03d}{ext.lower()}"
        file_path = os.path.join(base_dir, filename)

        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                existing_hash = hashlib.md5(f.read()).hexdigest()
            if existing_hash == content_hash:
                # Déjà présent
                return JsonResponse({"location": f"{base_url}/{filename}"})
            else:
                index += 1
        else:
            break

    # Sauvegarde réelle
    with open(file_path, "wb+") as dest:
        for chunk in image.chunks():
            dest.write(chunk)

    return JsonResponse({"location": f"{base_url}/{filename}"})
