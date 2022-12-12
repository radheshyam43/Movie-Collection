import pytest
from django.urls import reverse
from rest_framework import status

REGISTER_URL = reverse('register')
TOKEN_URL = reverse('token')

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "username, password, response_status",
    [
        ("JohnSmith", "Password123", status.HTTP_201_CREATED),
        ("John Smith", "Password123", status.HTTP_400_BAD_REQUEST),
    ]
)
def test_register_user_with_valid_username(client, username, password, response_status):
    payload = dict(
        username=username,
        password=password
    )
    response = client.post(REGISTER_URL, payload)

    assert response.status_code == response_status


def test_register_user_with_unique_username(client):
    payload = dict(
        username="JohnSmith",
        password="Password123"
    )
    client.post(REGISTER_URL, payload)
    response = client.post(REGISTER_URL, payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_token_valid_username_password(client):
    payload = dict(
        username="JohnSmith",
        password="Password123"
    )

    client.post(REGISTER_URL, payload)
    token_response = client.post(TOKEN_URL, payload)

    assert 'access' in token_response.data
    assert token_response.status_code == status.HTTP_200_OK


def test_get_token_invalid_username_password(client):
    registration_payload = dict(
        username="JohnSmith",
        password="Password123"
    )

    token_payload = dict(
        username="JohnSmith1",
        password="Password123"
    )

    client.post(REGISTER_URL, registration_payload)
    token_response = client.post(TOKEN_URL, token_payload)

    assert 'access' not in token_response.data
    assert token_response.status_code == status.HTTP_401_UNAUTHORIZED
