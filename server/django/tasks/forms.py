from django import forms
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError



from .models import Task


def validate_not_in_range(value):
    if 1 <= value <= 49:
        raise ValidationError('1から49の値は許可されていません')

class TaskForm(forms.ModelForm):
    fine = forms.IntegerField(validators=[MaxValueValidator(100000), validate_not_in_range])
    class Meta:
        model = Task
        fields = ["title", "fine"]
