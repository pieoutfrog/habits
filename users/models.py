from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс Юзера"""
    chat_id = models.IntegerField(unique=True, verbose_name='Tg chat id')

    def save(self, *args, **kwargs):
        """Создание пароля и его хеширование"""
        self.set_password(self.password)
        super().save(*args, **kwargs)
