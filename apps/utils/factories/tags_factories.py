import factory
from faker import Faker
from apps.core.app_main.models.tags import Tag
import random
from django.utils.text import slugify

fake = Faker()

class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    @factory.lazy_attribute
    def name(self):
        use_two_words = random.random() < 0.9
        if use_two_words:
            mot1 = fake.word().capitalize()
            mot2 = fake.word().capitalize()
            full_name = f"{mot1} {mot2}"
        else:
            full_name = fake.word().capitalize()
        print(f"✔️ Tag généré : '{full_name}' (2 mots = {use_two_words})")
        return full_name

    @factory.lazy_attribute
    def slug(self):
        return slugify(self.name)

    description = factory.Faker("sentence")
    access_level = factory.LazyFunction(lambda: random.choice(list(Tag.ACCESS_LEVELS.values())))
