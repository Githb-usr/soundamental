import pytest
import pprint
from django.conf import settings
from django.db.models.signals import post_save
from apps.core.app_main.models.index import IndexEntry, PageExistence, IndexSettings
from django.core.exceptions import ValidationError
from unidecode import unidecode

def test_link_bases():
    """Vérifie que LINK_BASES contient bien les clés attendues."""
    print("\n🔍 Contenu actuel de settings.LINK_BASES :")
    pprint.pprint(settings.LINK_BASES)  # 🔹 Ajout pour debug
    assert hasattr(settings, "LINK_BASES"), "❌ settings n'a pas 'LINK_BASES'"
    assert "forum" in settings.LINK_BASES, "❌ LINK_BASES ne contient pas 'forum'"
    assert "artiste" in settings.LINK_BASES, "❌ LINK_BASES ne contient pas 'artiste'"

@pytest.mark.django_db
def test_index_entry_creation():
    """Test de la création d'une entrée dans l'index."""
    entry = IndexEntry.objects.create(name="Michael Jackson", category="artiste")
    assert entry.name == "Michael Jackson"
    assert entry.category == "artiste"

@pytest.mark.django_db
@pytest.mark.parametrize("category, name, forum_id, existing_pages, expected_keys", [
    ("artiste", "Daft Punk", "12345-daft-punk", ["biography", "discography"], ["biography", "discography", None, None, "forum"]),
    ("compilation", "Top DJ Hits", "54321-top-dj-hits", ["history", "volumes"], ["history", "volumes", None, None, "forum"]),
    ("label", "Epic Records", "98765-epic-records", ["history", "catalog"], ["history", "catalog", None, None, "forum"]),
])
def test_index_entry_links(category, name, forum_id, existing_pages, expected_keys):
    """Test de génération des liens dynamiques pour différentes catégories."""
    entry = IndexEntry.objects.create(name=name, category=category, id_forum=forum_id)

    # 🔹 Création des pages existantes
    for page in existing_pages:
        PageExistence.objects.create(category=category, name=name, page_type=f"{category}_{page}")

    expected_slug = f"{entry.id}-{entry.name.lower().replace(' ', '-')}"
    expected_links = [
        settings.LINK_BASES[category][key].format(expected_slug) if key else None
        for key in expected_keys[:-1]
    ] + [settings.LINK_BASES["forum"].format(forum_id)]

    assert entry.get_links == expected_links, f"❌ Liens incorrects pour {category}: {entry.get_links}"

@pytest.mark.django_db
def test_index_entry_invalid_category():
    """Test de la création d'une entrée avec une catégorie invalide."""
    entry = IndexEntry(name="Fake Artist", category="invalide")

    # 🔹 Django ne vérifie pas les choix en base, donc on valide l'objet avant de l'enregistrer.
    with pytest.raises(ValidationError):
        entry.full_clean()  # 🔹 Force la validation des champs

@pytest.mark.django_db
@pytest.mark.parametrize("existing_pages, expected_keys", [
    ([], [None, None, None, None, "forum"]),  # Aucune page existante
    (["biography", "discography"], ["biography", "discography", None, None, "forum"]),  # Seulement bio & disco
    (["biography", "discography", "videography", "bootography"], ["biography", "discography", "videography", "bootography", "forum"]),  # Toutes existent
])
def test_index_entry_links_existing_pages(existing_pages, expected_keys):
    """Test si get_links récupère bien les pages existantes pour une entrée donnée."""
    entry = IndexEntry.objects.create(name="Daft Punk", category="artiste", id_forum="12345-daft-punk")

    # 🔹 Création des pages existantes
    for page in existing_pages:
        PageExistence.objects.create(category="artiste", name="Daft Punk", page_type=f"artiste_{page}")

    expected_slug = f"{entry.id}-{entry.name.lower().replace(' ', '-')}"
    expected_links = [
        settings.LINK_BASES["artiste"][key].format(expected_slug) if key else None
        for key in expected_keys[:-1]
    ] + [settings.LINK_BASES["forum"].format("12345-daft-punk")]

    assert entry.get_links == expected_links, f"❌ Liens incorrects : {entry.get_links}"

@pytest.mark.django_db
@pytest.mark.parametrize("forum_id, expected_url", [
    ("12345-daft-punk", settings.LINK_BASES["forum"].format("12345-daft-punk")),
    (None, None),
])
def test_index_entry_forum_url(forum_id, expected_url):
    """Test de get_forum_url avec ou sans id_forum."""
    entry = IndexEntry.objects.create(name="Test Artist", category="artiste", id_forum=forum_id)
    assert entry.get_forum_url == expected_url, f"❌ URL incorrecte : {entry.get_forum_url}"

@pytest.mark.django_db
@pytest.mark.parametrize("name, forum_id, expected_url", [
    ("Jean-Michel Jarre", None, None),  # Cas où il n'y a pas d'ID forum
    ("No Forum Artist", None, None),  # Cas redondant supprimé
    ("Daft Punk", "12345-daft-punk", settings.LINK_BASES["forum"].format("12345-daft-punk")),
])
def test_index_entry_forum_url(name, forum_id, expected_url):
    """Test de get_forum_url avec ou sans id_forum."""
    entry = IndexEntry.objects.create(name=name, category="artiste", id_forum=forum_id)
    assert entry.get_forum_url == expected_url, f"❌ URL incorrecte : {entry.get_forum_url}"

@pytest.mark.django_db
def test_index_entry_links_existing_only():
    """Test si get_links ne retourne que les liens existants dans PageExistence."""
    entry = IndexEntry.objects.create(name="Daft Punk", category="artiste", id_forum="12345-daft-punk")

    # 🔹 Création de pages existantes (mais pas toutes)
    PageExistence.objects.create(category="artiste", name="Daft Punk", page_type="artiste_biography")
    PageExistence.objects.create(category="artiste", name="Daft Punk", page_type="artiste_discography")

    expected_slug = f"{entry.id}-{entry.name.lower().replace(' ', '-')}"
    expected_links = [
        settings.LINK_BASES["artiste"]["biography"].format(expected_slug),
        settings.LINK_BASES["artiste"]["discography"].format(expected_slug),
        None,  # Pas de vidéographie en base
        None,  # Pas de bootographie en base
        settings.LINK_BASES["forum"].format("12345-daft-punk"),
    ]

    assert entry.get_links == expected_links, f"❌ Liens incorrects : {entry.get_links}"

@pytest.mark.django_db
def test_index_entry_links_compilation_label():
    """Test de génération de liens pour une compilation et un label."""
    # 🔹 Création d'une compilation
    comp_entry = IndexEntry.objects.create(name="Top DJ Hits", category="compilation", id_forum="54321-top-dj-hits")
    PageExistence.objects.create(category="compilation", name="Top DJ Hits", page_type="compilation_history")

    comp_expected_slug = f"{comp_entry.id}-{comp_entry.name.lower().replace(' ', '-')}"
    comp_expected_links = [
        settings.LINK_BASES["compilation"]["history"].format(comp_expected_slug),
        None,  # Pas de volumes en base
        None,  # Pas de vidéographie en base
        None,  # Pas de bootographie en base
        settings.LINK_BASES["forum"].format("54321-top-dj-hits"),
    ]
    assert comp_entry.get_links == comp_expected_links, f"❌ Liens incorrects pour compilation : {comp_entry.get_links}"

    # 🔹 Création d'un label
    label_entry = IndexEntry.objects.create(name="Warner Music", category="label", id_forum="98765-warner-music")
    PageExistence.objects.create(category="label", name="Warner Music", page_type="label_history")
    PageExistence.objects.create(category="label", name="Warner Music", page_type="label_catalog")

    label_expected_slug = f"{label_entry.id}-{label_entry.name.lower().replace(' ', '-')}"
    label_expected_links = [
        settings.LINK_BASES["label"]["history"].format(label_expected_slug),
        settings.LINK_BASES["label"]["catalog"].format(label_expected_slug),
        None,  # Pas d'autre lien en base
        None,  # Pas de bootographie en base
        settings.LINK_BASES["forum"].format("98765-warner-music"),
    ]
    assert label_entry.get_links == label_expected_links, f"❌ Liens incorrects pour label : {label_entry.get_links}"

@pytest.mark.django_db
def test_index_entry_special_characters():
    """Test de gestion des noms avec caractères spéciaux."""
    entry = IndexEntry.objects.create(name="Mötley Crüe", category="artiste", id_forum="55555-motley-crue")
    PageExistence.objects.create(category="artiste", name="Mötley Crüe", page_type="artiste_biography")

    # 🔹 Génération du slug attendu en normalisant les caractères spéciaux
    expected_slug = f"{entry.id}-{unidecode(entry.name).lower().replace(' ', '-')}"

    expected_links = [
        settings.LINK_BASES["artiste"]["biography"].format(expected_slug),
        None,  # Pas de discographie en base
        None,  # Pas de vidéographie en base
        None,  # Pas de bootographie en base
        settings.LINK_BASES["forum"].format("55555-motley-crue"),
    ]

    assert entry.get_links == expected_links, f"❌ Slug incorrect : {entry.get_links}"

@pytest.mark.django_db
def test_index_entry_no_pages():
    """Test du comportement quand une page n'existe pas dans PageExistence."""
    entry = IndexEntry.objects.create(name="Daft Punk", category="artiste", id_forum="12345-daft-punk")

    expected_slug = f"{entry.id}-{entry.name.lower().replace(' ', '-')}"
    
    expected_links = [
        None,  # Pas de biographie
        None,  # Pas de discographie
        None,  # Pas de vidéographie
        None,  # Pas de bootographie
        settings.LINK_BASES["forum"].format("12345-daft-punk"),  # Lien forum valide
    ]

    assert entry.get_links == expected_links, f"❌ Liens incorrects : {entry.get_links}"

@pytest.mark.django_db
def test_index_entry_deletion_on_page_removal():
    """Test de la suppression d'une entrée dans IndexEntry quand toutes ses pages sont supprimées."""
    entry = IndexEntry.objects.create(name="Daft Punk", category="artiste", id_forum="12345-daft-punk")

    # 🔹 Ajouter des pages associées
    PageExistence.objects.create(category="artiste", name="Daft Punk", page_type="artiste_biography")
    PageExistence.objects.create(category="artiste", name="Daft Punk", page_type="artiste_discography")

    # Vérifier que l'entrée existe bien
    assert IndexEntry.objects.filter(name="Daft Punk").exists(), "❌ L'entrée IndexEntry aurait dû être présente."

    # 🔹 Supprimer toutes les pages
    PageExistence.objects.filter(name="Daft Punk").delete()

    # Vérifier que l'entrée IndexEntry a bien été supprimée
    assert not IndexEntry.objects.filter(name="Daft Punk").exists(), "❌ L'entrée IndexEntry aurait dû être supprimée."

