from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import LoginAttempt

User = get_user_model()


class LimitLoginBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # ユーザー名でユーザーを検索
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # ユーザーが存在しない場合はNoneを返す
            return None

        # ユーザーがスーパーユーザーでなければ、通常の認証プロセスを続行
        if not user.is_superuser:
            return super().authenticate(request, username=username, password=password, **kwargs)

        # ログイン試行を追跡するオブジェクトを取得または作成
        login_attempt, _ = LoginAttempt.objects.get_or_create(user=user)

        # アカウントがロックされているかチェック
        if login_attempt.attempts >= 10:
            # アカウントがロックされている場合はエラーを発生
            raise ValidationError("このアカウントはロックされています。")

        # パスワードの検証
        if user.check_password(password):
            # ログイン成功
            login_attempt.attempts = 0
            login_attempt.save()
            return user
        else:
            # ログイン失敗
            login_attempt.attempts += 1
            login_attempt.last_attempt = timezone.now()
            login_attempt.save()
            return None
