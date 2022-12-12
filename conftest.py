import pytest
from accounts.utils import get_tokens_for_user
from collection.tests.factories import (CollectionFactory, MovieFactory,
                                        UserFactory)
from pytest_factoryboy import register
from rest_framework.test import APIClient

register(UserFactory)
register(UserFactory, "first_user", username="FirstUser")
register(MovieFactory)
register(CollectionFactory)


# It return anonymous client
@pytest.fixture
def client():
    return APIClient()


# returns client and user, where client is authorized using users JWT Token
@pytest.fixture()
def auth_client_and_user(first_user):
    client = APIClient()
    token = get_tokens_for_user(first_user)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token['access']))
    return client, first_user


# return a collection, client and user where, collection is owned by the user
@pytest.fixture()
def collection_with_client_and_user(collection_factory, movie_factory):
    client = APIClient()

    collection = collection_factory.create()
    movie = movie_factory.create()
    user = collection.user
    collection.movies.add(movie)

    token = get_tokens_for_user(user)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token['access']))
    return collection, client, user
