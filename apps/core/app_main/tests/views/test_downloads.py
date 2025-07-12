import pytest
from django.urls import reverse
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.core.app_main.models.downloads import DownloadableFile, DownloadLog
from apps.core.app_main.models.tags import Tag
from apps.core.app_main.models.dynamic_pages import DynamicPageTag


@pytest.mark.django_db
def test_telechargements_view(client):
    """Test que la vue des téléchargements affiche bien les fichiers et les tags."""
    
    # Création de fichiers téléchargeables
    file1 = DownloadableFile.objects.create(title="Fichier A", download_count=5)
    file2 = DownloadableFile.objects.create(title="Fichier B", download_count=2)

    # Création d'un tag et association avec la page "telechargements"
    tag = Tag.objects.create(name="Important")
    DynamicPageTag.objects.create(tag=tag, page_name="telechargements")

    response = client.get(reverse("app_main:telechargements"))

    assert response.status_code == 200
    assert "files" in response.context
    assert "tags" in response.context

    # Vérifier que les fichiers sont bien présents dans le contexte
    assert list(response.context["files"]) == [file1, file2]

    # Vérifier que le tag est bien récupéré
    assert tag in response.context["tags"]


@pytest.mark.django_db
@pytest.mark.parametrize("sort_param, expected_order", [
    ("uploaded_at", "uploaded_at"),
    ("-uploaded_at", "-uploaded_at"),
    ("title", "title"),
    ("-title", "-title"),
    ("download_count", "download_count"),
    ("-download_count", "-download_count"),
])
def test_telechargements_view_sorting(client, sort_param, expected_order):
    """Test que le tri des fichiers fonctionne correctement."""

    # Création de fichiers avec des valeurs différentes
    file1 = DownloadableFile.objects.create(title="Alpha", download_count=3)
    file2 = DownloadableFile.objects.create(title="Beta", download_count=1)
    file3 = DownloadableFile.objects.create(title="Charlie", download_count=2)

    response = client.get(reverse("app_main:telechargements"), {"sort": sort_param})

    assert response.status_code == 200
    files = list(response.context["files"])

    # Vérification de l'ordre attendu
    if expected_order == "title":
        assert files == [file1, file2, file3]
    elif expected_order == "-title":
        assert files == [file3, file2, file1]
    elif expected_order == "download_count":
        assert files == [file2, file3, file1]
    elif expected_order == "-download_count":
        assert files == [file1, file3, file2]


@pytest.mark.django_db
def test_download_file(client):
    """Test que le téléchargement d'un fichier fonctionne et incrémente le compteur."""

    # 🔹 Création d'un fichier factice
    fake_file = SimpleUploadedFile("test_file.txt", b"Fake content", content_type="text/plain")

    # 🔹 Création de l'objet avec un fichier
    file = DownloadableFile.objects.create(title="Test File", file=fake_file, download_count=0)

    # 🔹 Mock de l'ouverture du fichier pour éviter les erreurs d'accès
    with patch.object(file.file, "open", return_value=fake_file.file) as mock_open:
        response = client.get(reverse("app_main:download_file", args=[file.id]))

    # 🔹 Vérifications
    assert response.status_code == 200  # Le fichier doit être accessible
    file.refresh_from_db()
    assert file.download_count == 1  # Vérifier que le compteur de téléchargement a bien augmenté
