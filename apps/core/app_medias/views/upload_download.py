# apps/core/app_medias/views/upload_download.py

import os
import hashlib
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.text import slugify
from django.core.files.uploadedfile import UploadedFile

@csrf_exempt
@require_POST
@login_required
def upload_image_download(request):
    """
    Upload d’image pour illustrer un fichier à télécharger.
    Les fichiers sont stockés dans /media/downloads/
    """
    if not request.META.get("HTTP_X_CSRFTOKEN"):
        return HttpResponseForbidden("CSRF token manquant.")

    image: UploadedFile = request.FILES.get("image")
    if not image:
        return HttpResponseBadRequest("Aucun fichier envoyé.")

    base_dir = os.path.join(settings.MEDIA_ROOT, "downloads", "images")
    base_url = os.path.join(settings.MEDIA_URL, "downloads", "images")

    os.makedirs(base_dir, exist_ok=True)

    content_hash = hashlib.md5(image.read()).hexdigest()
    image.seek(0)

    name, ext = os.path.splitext(image.name)
    base_name = slugify(name) or "image"
    index = 1

    while True:
        filename = f"{base_name}_{index:03d}{ext.lower()}"
        file_path = os.path.join(base_dir, filename)
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                existing_hash = hashlib.md5(f.read()).hexdigest()
            if existing_hash == content_hash:
                return JsonResponse({"location": f"{base_url}/{filename}"})
            else:
                index += 1
        else:
            break

    with open(file_path, "wb+") as dest:
        for chunk in image.chunks():
            dest.write(chunk)

    return JsonResponse({"location": f"{base_url}/{filename}"})
