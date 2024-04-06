import uuid

from django.conf import settings
from django.db import models


class Task(models.Model):
    IN_PROGRESS = "I"
    DONE = "D"
    FAILED = "F"

    STATUS_CHOICES = {
        IN_PROGRESS: "In Progress",
        DONE: "Done",
        FAILED: "Failed",
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    fine = models.PositiveIntegerField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=IN_PROGRESS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " - " + self.created_at.strftime("%Y/%m/%d %H:%M:%S")


class Todo(models.Model):
    IN_PROGRESS = "I"
    DONE = "D"
    FAILED = "F"
    STOPPED = "S"

    STATUS_CHOICES = {
        IN_PROGRESS: "In Progress",
        DONE: "Done",
        FAILED: "Failed",
        STOPPED: "Stopped",
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=IN_PROGRESS)

    def __str__(self):
        return self.task.title + " - " + str(self.date)