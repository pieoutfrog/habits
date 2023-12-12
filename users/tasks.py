from datetime import timedelta

from django.utils import timezone

from celery import shared_task

from users.models import User


@shared_task
def user_activity():
    users = User.objects.all()
    for user in users:
        if user.last_login:
            if timezone.now() - user.last_login > timedelta(days=30):
                user.is_active = False
                user.save()

