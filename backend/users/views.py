from rest_framework import generics, authentication
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from api.serializers import (UserSerializer,
                             StudentSerializer,
                             CoachSerializer,
                             AuthTokenSerializer)


class CreateUserView(generics.CreateAPIView):
    permission_classes = [IsAdminUser,]
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CreateStudentView(generics.CreateAPIView):
    authentication_classes  = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer


class CreateCoachView(generics.CreateAPIView):
    authentication_classes  = [authentication.TokenAuthentication]
    serializer_class = CoachSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes  = [authentication.TokenAuthentication]

    def get_object(self):
        return self.request.user