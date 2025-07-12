"""
##############################################################
# GÉNÉRATION DE DONNÉES FACTICES POUR LE BLOG (USAGE EXCEPTIONNEL)
##############################################################

Ce fichier permet de générer des articles de blog fictifs
pour les tests ou la phase de développement local.

🛑 Ne jamais utiliser en production.

✅ CONDITIONS REQUISES AVANT L’UTILISATION :
- Avoir au moins une catégorie en base (catégories d’article)
- Un superutilisateur doit exister (il sera utilisé comme auteur)
- DISABLE_SIGNALS peut rester à True, aucun signal requis ici

✅ POUR LANCER LA GÉNÉRATION :
Depuis le shell Django :

from apps.utils.factories.blog_factories import generate_fake_articles
generate_fake_articles(20)

⚠️ Si aucune catégorie n’est présente, la génération plantera.
⚠️ Des tags peuvent être ajoutés plus tard si nécessaire.
"""

import factory
import random
from django.utils.text import slugify
from django.utils import timezone
from apps.content.app_blog.models import Article
from apps.content.app_blog.models.category import CategorieArticle
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()
fake = Faker()


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    titre = factory.Faker("sentence", nb_words=5)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.titre))
    contenu = factory.Faker("paragraph", nb_sentences=8)
    resume = factory.Faker("sentence", nb_words=10)
    date_publication = factory.LazyFunction(lambda: timezone.make_aware(fake.date_time_between(start_date='-5y', end_date='now')))
    auteur = factory.LazyFunction(lambda: User.objects.filter(is_superuser=True).first())
    est_publie = True

    # ⚠️ Catégorie principale obligatoire (prise parmi celles déjà en base)
    @factory.lazy_attribute
    def categorie_principale(self):
        categories = CategorieArticle.objects.all()
        if not categories.exists():
            raise Exception("❌ Aucune catégorie d'article trouvée. Créez-en une dans l'admin ou via une factory.")
        return random.choice(list(categories))

    # Catégories secondaires aléatoires (0 à 2)
    @factory.post_generation
    def categories_secondaires(self, create, extracted, **kwargs):
        if not create:
            return
        possibles = CategorieArticle.objects.exclude(pk=self.categorie_principale.pk)
        secondaires = possibles.order_by('?')[:random.randint(0, 2)]
        self.categories_secondaires.set(secondaires)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Sauvegarde forcée manuelle avec update_fields pour date_publication
        date_publication = kwargs.get('date_publication')
        obj = model_class(*args, **kwargs)
        obj.save(force_insert=True)

        if date_publication:
            obj.date_publication = date_publication
            obj.save(update_fields=['date_publication'])

        return obj


def generate_fake_articles(nb=20):
    """
    Génère un nombre donné d'articles fictifs.
    """
    for _ in range(nb):
        ArticleFactory()

    print(f"✅ {nb} articles générés.")
