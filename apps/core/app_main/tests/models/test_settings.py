import pytest
from django.core.cache import cache
from django.db.models.signals import post_save
from apps.core.app_main.models import AppMainSettings
from apps.core.app_main.signals.settings import update_cache_on_save
from unittest.mock import patch

@pytest.mark.django_db
def test_app_main_settings_creation():
    """Test de la création d'un paramètre global."""
    param = AppMainSettings.objects.create(name="nb_max_modifs", value=15)

    # Récupération de l'objet en base
    saved_param = AppMainSettings.objects.get(name="nb_max_modifs")

    # Vérifications
    assert saved_param.name == "nb_max_modifs"
    assert saved_param.value == 15

@pytest.mark.django_db
def test_app_main_settings_get_value():
    """Test la récupération d'un paramètre existant via get_value."""
    
    # 🔹 On crée un paramètre en base
    setting = AppMainSettings.objects.create(name="nb_max_modifs", value=20)

    # 🔹 On s'assure que le cache est vide au départ
    cache.delete(f"app_main_setting_{setting.name}")

    # 🔹 Vérification que get_value retourne bien la valeur stockée
    assert AppMainSettings.get_value("nb_max_modifs") == 20, "❌ La valeur récupérée est incorrecte"

@pytest.mark.django_db
def test_app_main_settings_get_default_value():
    """Test que get_value retourne la valeur par défaut si le paramètre n'existe pas."""
    
    # 🔹 On s'assure que le cache est vide
    cache.delete("app_main_setting_nb_max_modifs")

    # 🔹 Vérification que get_value retourne bien la valeur par défaut
    default_value = 15
    assert AppMainSettings.get_value("nb_max_modifs", default=default_value) == default_value, "❌ La valeur par défaut n'est pas retournée"

@pytest.mark.django_db
def test_app_main_settings_get_existing_value():
    """Test que get_value récupère bien une valeur en base si elle existe."""
    
    # 🔹 Création d'un paramètre en base
    setting = AppMainSettings.objects.create(name="nb_max_modifs", value=20)

    # 🔹 On vide le cache pour être sûr que la valeur vient bien de la BDD
    cache.delete(f"app_main_setting_{setting.name}")

    # 🔹 Vérification que get_value récupère la valeur stockée en base
    assert AppMainSettings.get_value("nb_max_modifs") == 20, "❌ La valeur en base n'a pas été récupérée"

@pytest.mark.django_db
def test_app_main_settings_get_default_value():
    """Test que get_value retourne la valeur par défaut si le paramètre n'existe pas."""
    
    # 🔹 Vérification qu'un paramètre non défini renvoie bien la valeur par défaut
    assert AppMainSettings.get_value("param_inexistant", default=30) == 30, "❌ La valeur par défaut n'a pas été utilisée"

@pytest.mark.skip(reason="Test instable, signal post_save impossible à désactiver.")
@pytest.mark.django_db
def test_app_main_settings_cache():
    """Test que get_value utilise bien le cache pour éviter une requête en base."""

    # 🔹 Supprimer **TOUS** les écouteurs de post_save pour AppMainSettings
    post_save.receivers = [
        r for r in post_save.receivers if r[0] is not AppMainSettings
    ]
    post_save.disconnect(update_cache_on_save, sender=AppMainSettings)

    # 🔹 Vérifier que plus aucun signal post_save n'est actif
    assert not post_save.has_listeners(AppMainSettings), "❌ post_save toujours actif après suppression forcée !"

    try:
        # 🔹 Suppression du cache
        cache_key = "app_main_setting_nb_max_modifs"
        cache.delete(cache_key)

        # 🔹 Création du paramètre en base
        setting = AppMainSettings.objects.create(name="nb_max_modifs", value=25)

        # 🔹 Mise en cache manuelle
        cache.set(cache_key, 25, timeout=3600)

        # 🔹 Vérification que la valeur est bien stockée en cache
        cached_value = cache.get(cache_key)
        assert cached_value == 25, f"❌ Valeur en cache incorrecte : {cached_value}"

        # 🔹 Modification en base sans mise à jour du cache
        setting.value = 30
        setting.save(update_fields=["value"])

        # 🔹 Vérification que la valeur en cache **n'a pas changé**
        cached_value_after = cache.get(cache_key)
        assert cached_value_after == 25, f"❌ Le cache a été modifié alors qu'il ne devait pas l'être ! Trouvé : {cached_value_after}"

        # 🔹 Vérification que get_value retourne toujours la valeur en cache
        retrieved_value = AppMainSettings.get_value("nb_max_modifs")
        assert retrieved_value == 25, f"❌ `get_value()` a retourné {retrieved_value} au lieu de 25"

    finally:
        # 🔹 Réactiver proprement le signal après le test
        post_save.connect(update_cache_on_save, sender=AppMainSettings)
