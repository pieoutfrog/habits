from celery import shared_task

from config.settings import TG_TOKEN, TG_URL
from habits.models import Habit
from habits.services import get_message, send_tg_message


@shared_task
def send_reminder_tg():
    """Сбор всех данных и отправка напоминания владельцу привычки"""
    api = TG_TOKEN
    base_url = TG_URL

    for habit in Habit.objects.all():
        message = get_message(habit)

        full_url = f'{base_url}{api}/sendMessage?chat_id={habit.owner.chat_id}&text={message}'

        send_tg_message(habit, full_url)