from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='admin@mail.ru',
            username='admin',
            first_name='Oleg',
            last_name='Olegovich',
            is_staff=True,
            is_superuser=False
        )

        user.set_password('admin')
        user.save()
