"""
Views for user app
"""

# Create your views here.
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import generics, authentication, permissions, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializer import UserImageSerializer, UserSerializer, AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


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


class UserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing users, including profile picture uploads.
    """

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    @action(methods=["POST"], detail=False, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """
        Upload an image for
        the authenticated user.
        """

        user = request.user
        serializer = UserImageSerializer(user, data=request.data, partial=True)
        # serializer = self.get_serializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
