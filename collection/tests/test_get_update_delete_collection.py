import pytest
import json
from django.urls import reverse
from rest_framework import status
from collection.models import Collection

pytestmark = pytest.mark.django_db


class TestGetCollectionAPI:

    def test_collection_detail_with_unauthorized_user(self, collection_with_client_and_user, client):
        '''
        Unauthorized user will get 401_UNAUTHORIZED response
        '''
        collection, auth_client, user = collection_with_client_and_user
        collection_detail_url = reverse('collection-details', args=[collection.uuid])
        collection_response = client.get(collection_detail_url)
        assert collection_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_collection_details_with_authorized_user(self, collection_with_client_and_user):
        '''
        Authorized User can see their own collection 
        '''
        collection, client, user = collection_with_client_and_user
        collection_detail_url = reverse('collection-details', args=[collection.uuid])
        collection_response = client.get(collection_detail_url)
        assert collection_response.status_code == status.HTTP_200_OK
        response_data = collection_response.data
        assert 'movies' in response_data
        assert 'title' in response_data and 'description' in response_data

    def test_collection_details_with_user_other_than_owner(self, collection_with_client_and_user, auth_client_and_user):
        '''
        Test Database have one collection which belongs to different user.
        Auth_user will get 403 forbidden response.  
        '''
        collection, client, user = collection_with_client_and_user
        collection_detail_url = reverse('collection-details', args=[collection.uuid])
        auth_client, auth_user = auth_client_and_user
        collection_response = auth_client.get(collection_detail_url)
        assert collection_response.status_code == status.HTTP_403_FORBIDDEN




class TestUpdateDeleteCollectionAPI:

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


    def test_update_collection_with_authorized_user(self, collection_with_client_and_user):
        '''
        Authorized User can update their own collection 
        '''
        collection, client, user = collection_with_client_and_user
        collection_detail_url = reverse('collection-details', args=[collection.uuid])
        update_collection_response = client.put(collection_detail_url, self.payload, format='json')
        assert update_collection_response.status_code == status.HTTP_200_OK
        
        response_data = update_collection_response.data
        assert response_data.get('title') == self.payload.get('title')
        assert response_data.get('description') == self.payload.get('description')
        assert len(response_data.get('movies')) == 2

    def test_delete_collection_with_authorized_user(self, collection_with_client_and_user):
        '''
        Authorized User can delete their own collection 
        '''
        collection, client, user = collection_with_client_and_user
        collection_detail_url = reverse('collection-details', args=[collection.uuid])
        assert len(user.collections.all()) == 1

        update_collection_response = client.delete(collection_detail_url)
        assert update_collection_response.status_code == status.HTTP_204_NO_CONTENT
        assert len(user.collections.all()) == 0
