# apps/core/app_medias/urls.py

from django.urls import path
from .views.upload_site import upload_image_site
from .views.upload_blog import upload_image_blog
from .views.browse_images import browse_images
from .views.file_insert_popup import media_images_insert_view
from .views.upload_form import upload_image_form_view

app_name = "app_medias"

urlpatterns = [
    # Uploads
    path("upload/site/", upload_image_site, name="upload_image_site"),
    path("upload/blog/", upload_image_blog, name="upload_image_blog"),

    # Navigation dans toutes les images
    path("browse/", browse_images, name="browse_images"),

    # Insertion dans TinyMCE (popup)
    path("insert/", media_images_insert_view, name="media_images_insert"),
    
    # Formulaire générique d'upload (site, pressages, artistes, etc.)
    path("<str:section>/upload/", upload_image_form_view, name="upload_form"),
]
