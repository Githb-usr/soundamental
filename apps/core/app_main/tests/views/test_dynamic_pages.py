import pytest
from unittest.mock import patch
from django.urls import reverse
from django.test import Client
from django.shortcuts import get_object_or_404
from apps.core.app_main.models.dynamic_pages import DynamicPageInfo
from apps.core.app_main.models.static_pages import StaticPageMeta
from apps.core.app_main.views.dynamic_pages import dynamic_page_view

@pytest.mark.django_db
def test_dynamic_page_with_display_name(client):
    """Test de l'affichage d'une page dynamique avec un display_name défini."""
    DynamicPageInfo.objects.create(page_name="custom-page", display_name="Custom Page")

    response = client.get(reverse("app_main:dynamic_page", args=["custom-page"]))

    print("\n🔍 DEBUG HTML (test_dynamic_page_with_display_name):\n", response.content.decode())  # 👈 Ajoute ce print
    print("\n🛠 CONTEXTE RÉPONSE:", response.context)

    assert response.status_code == 200
    assert "Custom Page" in response.content.decode()


@pytest.mark.django_db
def test_dynamic_page_without_display_name(client):
    """Test d'une page dynamique sans display_name (fallback sur page_name)."""
    DynamicPageInfo.objects.create(page_name="unknown-page")

    response = client.get(reverse("app_main:dynamic_page", args=["unknown-page"]))

    print("\n🔍 DEBUG HTML (test_dynamic_page_without_display_name):\n", response.content.decode())  # 👈 Ajoute ce print

    assert response.status_code == 200
    assert "Unknown Page" in response.content.decode()


@pytest.mark.django_db
def test_dynamic_page_redirects_to_static_if_exists(client):
    """Test d'une page dynamique qui existe en statique (doit rediriger vers static_page_view)."""
    StaticPageMeta.objects.create(title="A Propos", slug="a-propos", published=True)

    response = client.get(reverse("app_main:dynamic_page", args=["a-propos"]))

    assert response.status_code == 200
    assert "A Propos" in response.content.decode()

@pytest.mark.django_db
@patch("apps.core.app_main.views.index.index_or_category_view")
def test_dynamic_page_redirects_to_index(mock_index_view, client):
    """Test de la redirection vers index_or_category_view si page_name == 'index'."""
    
    response = client.get(reverse("app_main:dynamic_page", args=["index"]))

    print(f"\n🔍 MOCK CALL COUNT: {mock_index_view.call_count}")  # 👈 Vérifie si le mock est appelé

    assert mock_index_view.called  # Vérifie que la redirection a bien eu lieu

