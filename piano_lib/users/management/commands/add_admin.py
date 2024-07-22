from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    username = 'admin'
    password = 'adminpass'
    user = get_user_model().objects.filter(username=username).first()
    if not user:
        get_user_model().objects.create_superuser(
            username=username,
            password=password,
            email=''
        )
