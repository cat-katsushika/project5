import uuid

from django.db import models
from tasks.models import Task


class Supporter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)
    name = models.CharField(max_length=255)
    personality = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class EncouragementMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    supporter = models.ForeignKey(Supporter, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    day_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.supporter.name} for {self.task.title} on day {self.day_number}"
