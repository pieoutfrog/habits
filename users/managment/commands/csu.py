import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from users.models import User


def create_superuser():
    email = input("Enter email: ")
    password = input("Enter password: ")

    User.objects.create_superuser(email=email, password=password)
    print("Superuser created successfully.")


if __name__ == "__main__":
    create_superuser()
