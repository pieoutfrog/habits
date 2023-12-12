import datetime

import requests
from django.utils import timezone


def get_message(habit):
    """Создание напоминания пользователю"""
    if habit.reward:
        reward = habit.reward
    elif habit.connected_habit:
        reward = habit.connected_habit.action
    else:
        reward = 'Отсутствует'

    return (f'Уведомление о выполнении привычки! '
            f'\nВыполнить: {habit.action}. '
            f'\nМесто: {habit.place}. '
            f'\nВремя: {habit.time}. '
            f'\nВремя на выполнение: {habit.duration_of_action} секунд. '
            f'\nНаграда: {reward}.')


def send_tg_message(habit, full_url):
    """Проверка на наличие логов, их запись и отправка сообщения пользователю"""
    now = timezone.now()

    if habit.last_reminder:
        if habit.last_reminder <= now - datetime.timedelta(days=habit.period):
            requests.get(full_url)
            habit.last_reminder = timezone.now()
            habit.save()

    else:
        if habit.time <= now.time():
            requests.get(full_url)
            habit.last_reminder = timezone.now()
            habit.save()
