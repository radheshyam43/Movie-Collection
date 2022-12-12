from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Collection
from .permission import IsOwner
from .serializers import (CollectionListSerializer, CollectionSerializer,
                          CreateCollectionSerializer)
from .utils import get_favourite_geners


class CollectionList(generics.ListCreateAPIView):
    '''
    View used for creating and listing Collection/s for a user
    '''
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = CreateCollectionSerializer

    def get_queryset(self):
        user = self.request.user
        return user.collections.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CollectionListSerializer(queryset, many=True)
        updatedResponse = {
            "is_success": True,
            "data": {
                "collections": serializer.data,
                "favourite_genres": get_favourite_geners(queryset)
            }
        }
        return Response(updatedResponse)


class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    View used for Retrieving Updating and Deleting a particular Collection
    '''
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()
    lookup_url_kwarg = 'collection_uuid'

