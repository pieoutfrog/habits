from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    chat_id = models.IntegerField(unique=True, verbose_name='ТГ чат айди', **NULLABLE)
    username = None

    USERNAME_FIELD = 'chat_id'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        """Создание пароля и его хеширование"""
        self.set_password(self.password)
        super().save(*args, **kwargs)
