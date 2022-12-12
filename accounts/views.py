from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserRegistrationSerializer
from .utils import get_tokens_for_user


class UserRegistrationView(APIView):
    """
    Register new User to out databases

    Allowed request method: ['POST']

    Request Payload: {
        "username": "username",
        "password": "password"
    }
    """

    def post(self, request, format=None):

        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = get_tokens_for_user(user)

        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
