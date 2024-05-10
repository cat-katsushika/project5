from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    terms_accepted = forms.BooleanField(
        label="利用規約とプライバシーポリシーに同意する",
        required=True,  # このフィールドが必須であることを示します
        error_messages={"required": "利用規約とプライバシーポリシーに同意する必要があります。"},  # カスタムエラーメッセージ
    )
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "terms_accepted", "captcha")


class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]


class AdminOneTimePasswordForm(forms.Form):
    one_time_password = forms.CharField(label="ワンタイムパスワード", required=True, max_length=6)
