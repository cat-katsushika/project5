from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ContactForm


class ContactFormView(FormView):
    template_name = "contacts/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contacts:success")  # フォーム送信成功後のリダイレクト先

    def form_valid(self, form):
        form.save()  # フォームのデータをモデルに保存
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = "contacts/contact_success.html"


class NoticeView(TemplateView):
    template_name = "contacts/notice.html"
