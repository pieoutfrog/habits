from rest_framework import generics

from users.models import User
from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Эндпоинт создания(регистрация) юзера"""
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    """Эндпоинт просмотра всех юзеров"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Эндпоинт просмотра определенного юзера"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт редактирования юзера"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт удаления юзера"""
    queryset = User.objects.all()