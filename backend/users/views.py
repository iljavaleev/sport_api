from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import generics, authentication
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.settings import api_settings
from users.models import Coach, Student
from api.serializers import (UserSerializer,
                             StudentSerializer,
                             CoachSerializer,
                             ChangePasswordSerializer)
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404



class CreateUserView(generics.CreateAPIView):
    permission_classes = [IsAdminUser,]
    serializer_class = UserSerializer


class CreateWorker(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        request.data._mutable = True
        phone = request.data.pop('phone')[0]
        email = request.data.pop('email')[0]
        password = request.data.pop('password')[0]

        user = get_object_or_404(get_user_model(),
                                 email=email,
                                 phone=phone)

        request.data['user'] = user
        serializer = self.serializer_class(data=request.data)

        if (user.check_password(password)
                and serializer.is_valid(raise_exception=True)):
            serializer.save()
            token = Token.objects.create(user=user)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED)


class CreateStudentView(CreateWorker):
    serializer_class = StudentSerializer


class CreateCoachView(CreateWorker):
    serializer_class = CoachSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(
                    serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            token, created = Token.objects.get_or_create(user=self.object)
            token.delete()
            token = Token.objects.create(user=self.object)
            token.save()

            return Response({'token': token.key},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)