import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username

class LoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Attempts: {self.attempts}"
