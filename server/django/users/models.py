import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):

    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9.@+-]+$',
        message=_("ユーザー名には半角アルファベット、半角数字、および@/./+/-/_のみ使用できます。")
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        _("username"),
        max_length=15,
        unique=True,
        help_text="この項目は必須です。半角アルファベット、半角数字、@/./+/-/_ で15文字以下にしてください。",
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    def __str__(self):
        return self.username


class LoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Attempts: {self.attempts}"
