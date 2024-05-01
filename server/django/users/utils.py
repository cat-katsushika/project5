import secrets
import string

from django.contrib.auth import get_user_model


def generate_random_string(length=13):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def is_unique_username(username):
    User = get_user_model()
    return not User.objects.filter(username=username).exists()
