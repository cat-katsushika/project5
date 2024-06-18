from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ContactForm
from .models import Notice


class ContactFormView(FormView):
    template_name = "contacts/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contacts:success")  # フォーム送信成功後のリダイレクト先

    def form_valid(self, form):
        # モデルインスタンスを作成するが、まだデータベースには保存しない
        contact = form.save(commit=False)

        # ログインしている場合、ユーザー情報をmemoフィールドに追加
        if self.request.user.is_authenticated:
            memo_content = getattr(contact, "memo", "")  # 既存のmemo内容を取得（存在しなければ空文字）
            user_info = f"ユーザーid: {self.request.user.id}"  # ユーザー情報の文字列を作成
            contact.memo = f"{user_info}\n{memo_content}"  # 新しいmemo内容を設定

        contact.save()  # モデルのデータをデータベースに保存
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = "contacts/contact_success.html"


class NoticeView(TemplateView):
    template_name = "contacts/notice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        color = settings.DJANGO_ENV_COLOR
        context["env_color"] = (
            "text-bg-primary" if color == "blue" else "text-bg-success" if color == "green" else "text-bg-danger"
        )
        context["notices"] = Notice.objects.all().order_by("-created_at")
        return context
