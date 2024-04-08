from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    terms_accepted = forms.BooleanField(
        label="利用規約とプライバシーポリシーに同意する",
        required=True,  # このフィールドが必須であることを示します
        error_messages={'required': '利用規約とプライバシーポリシーに同意する必要があります。'},  # カスタムエラーメッセージ
    )
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "terms_accepted")

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
