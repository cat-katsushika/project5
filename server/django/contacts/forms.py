from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = Contact
        fields = ["name", "email", "message", "captcha"]
