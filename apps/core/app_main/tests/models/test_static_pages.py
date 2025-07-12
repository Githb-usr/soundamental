import pytest
from django.utils.text import slugify
from apps.core.app_main.models.static_pages import StaticPageMeta, StaticPageHistory
from apps.core.app_main.models.tags import Tag
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_static_page_creation():
    """Test la création d'une page statique et la génération automatique du slug."""

    user = User.objects.create(username="test_user")

    # 🔹 Création de la page statique
    page = StaticPageMeta.objects.create(
        title="Ma première page",
        content="Contenu de la page",
        created_by=user,
        updated_by=user
    )

    # 🔹 Vérification des valeurs enregistrées
    assert StaticPageMeta.objects.count() == 1, "❌ La page statique n'a pas été enregistrée"
    assert page.slug == slugify(page.title), f"❌ Slug incorrect : {page.slug}"

    # 🔹 Vérifie les relations
    assert page.created_by == user, "❌ L'utilisateur créateur est incorrect"
    assert page.updated_by == user, "❌ L'utilisateur modificateur est incorrect"

@pytest.mark.django_db
def test_static_page_modification_history():
    """Test que l'historique enregistre bien une modification d'une page statique."""

    user = User.objects.create(username="test_user")

    # 🔹 Création d'une page
    page = StaticPageMeta.objects.create(
        title="Page test",
        content="Contenu initial",
        created_by=user,
        updated_by=user
    )

    # 🔹 Vérification de l'historique après la création
    history_entries = StaticPageHistory.objects.filter(page=page)
    assert history_entries.count() == 1, "❌ Une entrée d'historique devrait être créée dès la création de la page"

    # 🔹 Modification de la page
    page.content = "Contenu modifié"
    page.updated_by = user
    page.save()

    # 🔹 Vérification de l'historique après modification
    history_entries = StaticPageHistory.objects.filter(page=page)
    assert history_entries.count() == 2, "❌ Une nouvelle entrée d'historique devrait être ajoutée après modification"

    latest_entry = history_entries.order_by("-modified_at").first()
    assert latest_entry.page == page, "❌ L'entrée d'historique ne correspond pas à la bonne page"
    assert latest_entry.modified_by == user, "❌ L'utilisateur modificateur est incorrect"

@pytest.mark.django_db
def test_static_page_update_creates_history():
    """Test que chaque modification d'une page statique ajoute bien une entrée dans l'historique."""

    user = User.objects.create(username="test_user")

    # 🔹 Création initiale d'une page
    page = StaticPageMeta.objects.create(
        title="Page modifiable",
        content="Contenu initial",
        created_by=user,
        updated_by=user
    )

    # 🔹 Vérifie que l'historique contient **une seule** entrée au départ (création)
    assert StaticPageHistory.objects.count() == 1, "❌ L'historique devrait contenir une seule entrée après création"

    # 🔹 Modification 1
    page.content = "Première modification"
    page.updated_by = user
    page.save()

    # 🔹 Modification 2
    page.content = "Deuxième modification"
    page.updated_by = user
    page.save()

    # 🔹 Vérifie que **chaque modification** a bien ajouté une entrée d'historique
    assert StaticPageHistory.objects.count() == 3, "❌ L'historique ne contient pas le bon nombre d'entrées"

    history_entries = StaticPageHistory.objects.filter(page=page).order_by("-modified_at")
    
    # 🔹 Vérifie que la dernière entrée correspond bien à la dernière modification
    assert history_entries[0].modified_by == user, "❌ L'utilisateur de la dernière modification est incorrect"

    print(f"✅ Historique correct avec {StaticPageHistory.objects.count()} entrées")

@pytest.mark.django_db
def test_static_page_creation_with_tags():
    """Test la création d'une page statique avec des tags."""

    user = User.objects.create(username="test_user")
    tag1 = Tag.objects.create(name="Electro")
    tag2 = Tag.objects.create(name="House")

    # 🔹 Création d'une page avec des tags
    page = StaticPageMeta.objects.create(
        title="Page avec tags",
        content="Contenu",
        created_by=user,
        updated_by=user
    )
    page.tags.add(tag1, tag2)

    # 🔹 Vérification des tags
    assert page.tags.count() == 2, "❌ Les tags ne sont pas correctement enregistrés"

    print("✅ Création avec tags OK")

@pytest.mark.django_db
def test_static_page_slug_update():
    """Test que le slug est mis à jour si le titre change."""

    user = User.objects.create(username="test_user")

    # 🔹 Création de la page
    page = StaticPageMeta.objects.create(
        title="Ancien Titre",
        content="Contenu",
        created_by=user,
        updated_by=user
    )

    # 🔹 Modification du titre
    page.title = "Nouveau Titre"
    page.updated_by = user
    page.save()

    # 🔹 Vérification du slug mis à jour
    assert page.slug == slugify("Nouveau Titre"), f"❌ Slug incorrect : {page.slug}"

    print("✅ Slug mis à jour correctement")

@pytest.mark.django_db
def test_static_page_deletion_cleans_history():
    """Test que la suppression d'une page supprime son historique."""

    user = User.objects.create(username="test_user")

    # 🔹 Création de la page
    page = StaticPageMeta.objects.create(
        title="Page temporaire",
        content="Contenu",
        created_by=user,
        updated_by=user
    )

    # 🔹 Vérification de l'historique (création)
    assert StaticPageHistory.objects.count() == 1, "❌ L'historique devrait contenir une seule entrée après création"

    # 🔹 Suppression de la page
    page.delete()

    # 🔹 Vérification que l'historique est bien supprimé
    assert StaticPageHistory.objects.count() == 0, "❌ L'historique n'a pas été supprimé avec la page"

    print("✅ Suppression de la page et nettoyage de l'historique OK")

@pytest.mark.django_db
def test_static_page_absolute_url():
    """Test que get_absolute_url retourne bien l'URL correcte."""

    user = User.objects.create(username="test_user")

    # 🔹 Création de la page
    page = StaticPageMeta.objects.create(
        title="Ma Page",
        content="Contenu",
        created_by=user,
        updated_by=user
    )

    # 🔹 Vérification de l'URL générée
    expected_url = f"/{page.slug}/"
    assert page.get_absolute_url() == expected_url, f"❌ URL incorrecte : {page.get_absolute_url()}"

    print("✅ URL générée correctement")

@pytest.mark.django_db
def test_static_page_default_published():
    """Test que la valeur par défaut du champ published est True."""
    user = User.objects.create(username="test_user")

    page = StaticPageMeta.objects.create(
        title="Page publiée par défaut",
        content="Contenu",
        created_by=user,
        updated_by=user
    )

    assert page.published is True, "❌ La page devrait être publiée par défaut !"
    print("✅ Le champ `published` est bien True par défaut")
