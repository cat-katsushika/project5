from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    memo = models.TextField("運営者用メモ欄", blank=True)

    def __str__(self):
        return self.name
