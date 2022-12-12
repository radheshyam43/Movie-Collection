import uuid

import factory
from collection.models import Collection, Movie
from django.contrib.auth.models import User
from faker import Faker
from faker.providers import DynamicProvider


genre_provider = DynamicProvider(
    provider_name="genre",
    elements=["Horror", "Romantic", "Science", "Thriller", "Drama"],
)

fake = Faker()

fake.add_provider(genre_provider)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.user_name()


class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    title = fake.name()
    uuid = str(uuid.uuid4())
    description = fake.text()
    genres = fake.genre()


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    title = fake.name()
    description = fake.text()
    user = factory.SubFactory(UserFactory)
