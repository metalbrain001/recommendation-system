"""
Views for user app
"""

# Create your views here.
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializer import UserSerializer, AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system
    """

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
    Create a new auth token for user
    """

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class LoginUserView(APIView):
    """
    Log in a user
    """

    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        Authenticate the user
        and return a token if valid.
        """

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # Create or retrieve a token for the user
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Manage the authenticated user
    """

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieve and return authenticated user
        """

        return self.request.user
