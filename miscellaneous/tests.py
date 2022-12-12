import pytest
from django.urls import reverse
from rest_framework import status

MOVIE_URL = reverse('movies')
REQUEST_COUNT_URL = reverse('request-count')
RESET_REQUEST_COUNT_URL = reverse('reset-request-count')

pytestmark = pytest.mark.django_db


@pytest.mark.skip
def test_movies_api(auth_client_and_user):
    client, user = auth_client_and_user
    response = client.get(MOVIE_URL)
    assert response.status_code == status.HTTP_200_OK


def test_request_count_url(auth_client_and_user):
    client, user = auth_client_and_user
    response = client.get(REQUEST_COUNT_URL)
    assert response.data.get('requests') == '1'

    response = client.get(REQUEST_COUNT_URL)
    assert response.data.get('requests') == '2'


def test_reset_request_count_url(auth_client_and_user):
    client, user = auth_client_and_user
    response = client.get(REQUEST_COUNT_URL)
    assert response.data.get('requests') == '1'

    client.post(RESET_REQUEST_COUNT_URL)
    response = client.get(REQUEST_COUNT_URL)
    assert response.data.get('requests') == '1'
