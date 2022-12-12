import pytest
import json
from django.urls import reverse
from rest_framework import status
from collection.models import Collection

COLLECTION_URL = reverse('collections')
pytestmark = pytest.mark.django_db


class TestGetCollectionAPI:

    def test_collection_list_with_unauthorized_user(self, collection_with_client_and_user, client):
        '''
        Unauthorized user will get 401_UNAUTHORIZED response
        '''
        collection_list_response = client.get(COLLECTION_URL)
        assert collection_list_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_collection_list_with_authorized_user(self, collection_with_client_and_user):
        '''
        Authorized User can see their own collection 
        '''
        collection, client, user = collection_with_client_and_user
        collection_list_response = client.get(COLLECTION_URL)
        assert collection_list_response.status_code == status.HTTP_200_OK

        response_data = collection_list_response.data
        assert response_data.get('is_success') == True
        assert len(response_data['data'].get('collections')) == 1

    def test_collection_list_with_user_other_than_owner(self, collection_with_client_and_user, auth_client_and_user):
        '''
        Test Database have one collection which belongs to different user.
        Auth_user will get 200_OK response with 0 collection.  
        '''
        auth_client, auth_user = auth_client_and_user
        collection_list_response = auth_client.get(COLLECTION_URL)
        assert collection_list_response.status_code == status.HTTP_200_OK

        response_data = collection_list_response.data
        assert response_data.get('is_success') == True
        assert Collection.objects.count() == 1 
        assert len(response_data['data'].get('collections')) == 0



class TestCreateCollectionAPI:

    payload = {
        "title": "Third Collection7",
        "description": "The Burkittsville and Shadow of the Blair Witch",
        "movies": [
            {
                "title": "The Burkittsville 7",
                "description": "A film archivist revisits the story of Rustin Parr",
                "genres": "Horror",
                "uuid": "5e904ce8-91b7-42b4-84d9-5b53f4cb8c74",
            }
        ]
    }

    def test_create_collection_with_unauthorized_user(self, client):
        '''
        Unauthorized user will get 401_UNAUTHORIZED response
        '''
        create_collection_response = client.post(COLLECTION_URL, self.payload)
        assert create_collection_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_collection_with_authorized_user(self, auth_client_and_user):
        '''
        Authorized User can create their own collection 
        '''
        client, user = auth_client_and_user
        create_collection_response = client.post(COLLECTION_URL, self.payload, format='json')
        assert create_collection_response.status_code == status.HTTP_201_CREATED

        response_data = create_collection_response.data
        assert response_data.get('collection_uuid')
