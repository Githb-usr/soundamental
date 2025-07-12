import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.core.app_main.models.downloads import DownloadableFile, DownloadLog

@pytest.mark.django_db
def test_file_creation():
    """Test : Création d'un fichier téléchargeable."""
    test_file = SimpleUploadedFile("test.pdf", b"Dummy content", content_type="application/pdf")
    downloadable_file = DownloadableFile.objects.create(
        title="Test File",
        description="Fichier de test",
        file=test_file
    )
    assert DownloadableFile.objects.count() == 1
    assert downloadable_file.title == "Test File"
    assert downloadable_file.description == "Fichier de test"

@pytest.mark.django_db
def test_register_download():
    """Test : Enregistrement d'un téléchargement."""
    test_file = SimpleUploadedFile("test.pdf", b"Dummy content", content_type="application/pdf")
    downloadable_file = DownloadableFile.objects.create(
        title="Test File",
        file=test_file
    )

    initial_count = downloadable_file.download_count
    downloadable_file.register_download()
    downloadable_file.refresh_from_db()

    assert downloadable_file.download_count == initial_count + 1
    assert DownloadLog.objects.filter(file=downloadable_file).count() == 1

@pytest.mark.django_db
def test_file_extension_validation():
    """Test : Vérification des extensions autorisées."""
    invalid_file = SimpleUploadedFile("test.exe", b"Invalid content", content_type="application/x-msdownload")

    with pytest.raises(ValidationError):
        invalid_download = DownloadableFile(title="Invalid File", file=invalid_file)
        invalid_download.full_clean()  # Déclenche la validation

@pytest.mark.django_db
def test_file_size_method():
    """Test : Vérification de la méthode get_file_size()."""
    test_file = SimpleUploadedFile("test.pdf", b"Dummy content", content_type="application/pdf")
    downloadable_file = DownloadableFile.objects.create(
        title="Test File",
        file=test_file
    )

    assert downloadable_file.get_file_size() >= 0
