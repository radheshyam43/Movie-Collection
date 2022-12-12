from django.conf import settings
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import KeyValueStore
from .utils import get_api_response


class GetMovies(APIView):
    """ 
    Hit third party api and redirect their response to user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        username = settings.MOVIE_API_USERNAME
        password = settings.MOVIE_API_PASSWORD
        url = settings.MOVIE_BASE_URL

        apiResponse = get_api_response(url, username, password)
        return Response(apiResponse.json())


class RequestCount(APIView):
    """
    Return number of request received by Server
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        request_count_object = KeyValueStore.objects.get(key='request_count')
        return Response({"requests": request_count_object.value})


class ResetRequestCount(APIView):
    """
    Reset number of request received by Server
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request_count_object = KeyValueStore.objects.select_for_update().get(key='request_count')
        with transaction.atomic():
            request_count_object.value = '0'
            request_count_object.save()

        return Response({"message": "request count reset successfully"})
