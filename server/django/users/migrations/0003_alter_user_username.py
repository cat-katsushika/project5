# Generated by Django 5.0.4 on 2024-04-13 10:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_loginattempt"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                error_messages={"unique": "A user with that username already exists."},
                help_text="この項目は必須です。半角アルファベット、半角数字、@/./+/-/_ で15文字以下にしてください。",
                max_length=15,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="ユーザー名には半角アルファベット、半角数字、および@/./+/-/_のみ使用できます。", regex="^[a-zA-Z0-9.@+-]+$"
                    )
                ],
                verbose_name="username",
            ),
        ),
    ]
