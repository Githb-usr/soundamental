import os
from pathlib import Path
from datetime import datetime

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods, require_GET
from django.template.response import TemplateResponse

from ..models import Article

@login_required
@user_passes_test(lambda u: u.is_staff or u.groups.filter(name="Contributeurs").exists())
def media_images_view(request):
    """
    Affiche les images TinyMCE uploadées dans blog/contenu/.
    Accessible uniquement aux admins et contributeurs.
    """
    image_folder = os.path.join(settings.MEDIA_ROOT, "blog", "contenu")
    images = []

    if os.path.exists(image_folder):
        for filename in sorted(os.listdir(image_folder)):
            file_path = os.path.join(image_folder, filename)
            if os.path.isfile(file_path) and filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".gif")):
                stat = os.stat(file_path)
                images.append({
                    "filename": filename,
                    "url": os.path.join(settings.MEDIA_URL, "blog", "contenu", filename),
                    "size_kb": stat.st_size // 1024,
                    "modified": datetime.fromtimestamp(stat.st_mtime),
                })

    context = {
        "images": images
    }
    return render(request, "app_blog/blog_images_list.html", context)


@staff_member_required
@require_http_methods(["GET", "POST"])
def delete_blog_image(request, filename):
    """
    Vue de confirmation + suppression d’une image du dossier blog/contenu/ (admin uniquement).
    """
    file_path = os.path.join(settings.MEDIA_ROOT, "blog", "contenu", filename)
    file_url = os.path.join(settings.MEDIA_URL, "blog", "contenu", filename)

    if request.method == "POST":
        if os.path.exists(file_path):
            os.remove(file_path)
            messages.success(request, f"L’image « {filename} » a été supprimée.")
        else:
            messages.error(request, f"Fichier introuvable : {filename}")
        return redirect("app_blog:blog_media_images")

    articles_utilisant_image = Article.objects.filter(
        contenu__icontains=filename
    ).only("id", "titre", "slug")

    context = {
        "filename": filename,
        "file_url": file_url,
        "articles_utilisant_image": articles_utilisant_image,
    }
    return TemplateResponse(request, "app_blog/confirm_delete_image.html", context)
