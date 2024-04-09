import uuid

from django.db import models
from tasks.models import Task


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    payment_intent_id = models.CharField(max_length=50, null=True)
    checkout_session_id = models.CharField(max_length=100)

    def __str__(self):
        return self.task.title
