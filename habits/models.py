from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    objects = models.Manager()
    HABIT_QREQUENCY_CHOICES = (
        ('daily', 'Ежедневная'),
        ('weekly', 'Еженедельная'),
        ('monthly', 'Ежемесячная'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец привычки', **NULLABLE)
    place = models.CharField(max_length=150, verbose_name='Место привычки')
    time = models.TimeField(verbose_name='Время')
    activity = models.CharField(verbose_name='Действие')
    sign_of_a_pleasant_habit = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    associated_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Связанная привычка', **NULLABLE)
    frequency = models.CharField(max_length=100, choices=HABIT_QREQUENCY_CHOICES, default='daily',
                                 verbose_name='Периодичность')
    reward = models.TextField(verbose_name='Вознаграждение')
    duration_of_action = models.IntegerField(verbose_name='Длительность привычки в секундах')
    is_public = models.BooleanField(default=False, verbose_name='Признак публичности привычки')
    last_reminder = models.DateTimeField(verbose_name='Последнее напоминание', **NULLABLE)

    def __str__(self):
        return f'Я буду {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
