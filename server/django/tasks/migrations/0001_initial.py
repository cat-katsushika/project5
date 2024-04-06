# Generated by Django 5.0.4 on 2024-04-05 11:30

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("fine", models.PositiveIntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[("I", "In Progress"), ("D", "Done"), ("F", "Failed")],
                        default="I",
                        max_length=1,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Todo",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("date", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("N", "Not Started"),
                            ("I", "In Progress"),
                            ("D", "Done"),
                            ("F", "Failed"),
                            ("S", "Stopped"),
                        ],
                        default="N",
                        max_length=1,
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tasks.task"
                    ),
                ),
            ],
        ),
    ]