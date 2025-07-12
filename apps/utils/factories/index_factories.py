"""
####################################################################
# GÉNÉRATION DE DONNÉES FACTICES POUR L'INDEX (USAGE EXCEPTIONNEL) #
####################################################################

Ce fichier sert uniquement à générer des données fictives pour les tests
ou la phase de développement local. Il ne doit pas être utilisé en production.

🛑 Important :
Les signaux Django (post_save/post_delete) doivent être actifs
pour que les entrées dans IndexEntry soient créées automatiquement
lors de la création des objets PageExistence.

✅ CONDITIONS REQUISES AVANT L’UTILISATION :
- DISABLE_SIGNALS = False dans les fichiers .env ou settings
- Ne pas exécuter ce code avant que Django ait bien enregistré les signaux

✅ POUR LANCER LA GÉNÉRATION :
Depuis le shell Django :

import apps.core.app_index.signals.index
from apps.utils.factories.index_factories import generate_fake_index_entries
generate_fake_index_entries(50)

💡 Une seule ligne est créée dans IndexEntry par nom unique.
Chaque nom peut ensuite avoir 1 à 4 pages (types différents)
générées dans PageExistence.

⚠️ Ce script ne modifie aucune donnée réelle.
Il peut être supprimé ou désactivé une fois les tests terminés.
"""

import factory
from faker import Faker
from apps.core.app_index.models import PageExistence
from apps.core.app_index.models import IndexEntry
import random

fake = Faker()

# Dictionnaire pour relier chaque catégorie à ses page_types possibles
PAGE_TYPES_BY_CATEGORY = {
    "artiste": [
        "artiste_biography",
        "artiste_discography",
        "artiste_videography",
        "artiste_bootography",
    ],
    "compilation": [
        "compilation_history",
        "compilation_volumes",
        "compilation_videography",
        "compilation_bootography",
    ],
    "label": [
        "label_history",
        "label_catalog",
        "label_bootography",
    ],
}

class PageExistenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PageExistence

    category = factory.LazyFunction(lambda: fake.random_element(elements=list(PAGE_TYPES_BY_CATEGORY.keys())))
    name = factory.Faker("name")  # ⚠️ Un nom générique, on pourra ajuster plus tard

    @factory.lazy_attribute
    def page_type(self):
        return fake.random_element(PAGE_TYPES_BY_CATEGORY[self.category])

def generate_fake_index_entries(nb=30):
    """
    Crée `nb` entrées uniques dans l'index, avec entre 1 et 4 pages associées
    pour générer dynamiquement les liens visibles.
    """
    noms_utilisés = set()

    for _ in range(nb):
        # Génère un nom enrichi avec un suffixe aléatoire pour éviter les doublons
        while True:
            base_name = fake.name()
            suffixe = fake.unique.lexify(text='????')  # Ajoute un suffixe de 4 lettres
            nom = f"{base_name} {suffixe}"
            if nom not in noms_utilisés:
                noms_utilisés.add(nom)
                break

        # Catégorie aléatoire
        categorie = random.choice(list(PAGE_TYPES_BY_CATEGORY.keys()))
        page_types = PAGE_TYPES_BY_CATEGORY[categorie]
        nb_pages = random.randint(1, min(4, len(page_types)))

        # Choisir des pages aléatoires à créer
        pages_choisies = random.sample(page_types, nb_pages)

        for page_type in pages_choisies:
            PageExistence.objects.create(
                category=categorie,
                name=nom,
                page_type=page_type
            )

        # Facultatif : ajouter un ID de forum pour ~30 % des entrées
        if random.random() < 0.3:
            entry = IndexEntry.objects.get(name=nom)
            fake_id = str(random.randint(1000, 99999))
            slug_part = nom.lower().replace(" ", "-")
            entry.id_forum = f"{fake_id}-{slug_part}"
            entry.save()

    print(f"✅ {nb} entrées générées pour l'index.")
