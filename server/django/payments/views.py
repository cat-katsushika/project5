import stripe

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from tasks.models import Task
from tasks.utils import send_message_to_discord

from .models import Payment


def create_checkout_session_view(request, pk):
    task = Task.objects.get(pk=pk)
    if task is None:
        return redirect("users:home")

    if Payment.objects.filter(task=task).exists():
        return redirect("users:home")

    relative_success_url = reverse("payments:success", kwargs={"pk": task.id})
    relative_cancel_url = reverse("payments:cancel", kwargs={"pk": task.id})
    success_url = request.build_absolute_uri(relative_success_url)
    cancel_url = request.build_absolute_uri(relative_cancel_url)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    # stripeのcheckout sessionのメールを設定，blankはエラーになるためNoneを設定
    email = task.user.email
    if not email:
        email = None

    session = stripe.checkout.Session.create(
        customer_email=email,
        line_items=[
            {
                "price_data": {
                    "currency": "jpy",
                    "product_data": {
                        "name": task.title,
                        "description": "5日間の継続を達成しましょう！5日間の継続に成功した場合，支払いは実行されません",
                    },
                    "unit_amount": task.fine,
                },
                "quantity": 1,
            }
        ],
        metadata={"user_id": task.user.id, "task_id": task.id},
        mode="payment",
        payment_intent_data={"capture_method": "manual"},
        success_url=success_url,
        cancel_url=cancel_url,
    )

    Payment.objects.create(
        task=task,
        payment_intent_id=session.payment_intent,
        checkout_session_id=session.id,
    )

    return redirect(session.url)


class PaymentSuccessView(TemplateView):
    template_name = "payments/success.html"

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs["pk"])
        if task is None:
            return redirect("users:home")

        if not Payment.objects.filter(task=task).exists():
            return redirect("users:home")

        # 罰金額が0の場合はpayment_intent_idがないため，そのままタスクを進行中にする
        if task.fine != 0:
            payment = Payment.objects.get(task=task)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            session = stripe.checkout.Session.retrieve(payment.checkout_session_id)
            payment.payment_intent_id = session.payment_intent
            payment.save()

            payment_intent = stripe.PaymentIntent.retrieve(payment.payment_intent_id)
            if payment_intent.status != "requires_capture":
                task.delete()
                return redirect("users:home")

        task.status = Task.IN_PROGRESS
        task.save()

        todos = task.todo_set.all()
        for todo in todos:
            todo.status = todo.IN_PROGRESS
            todo.save()

        # Discordに通知
        log_message_list = [
            " ============================= ",
            "タスクが生成されました",
            f"ユーザー名: {task.user.username}",
            f"タスク名　: {task.title}",
            f"罰金額　　: ¥{task.fine:,.0f}",
        ]
        log_message = "\n".join(log_message_list)
        send_message_to_discord(text=log_message, username="継続or罰金 タスク生成検知", avatar_url="")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = Task.objects.get(pk=kwargs["pk"])
        return context


class PaymentCancelView(TemplateView):
    template_name = "payments/cancel.html"

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs["pk"])
        if task is None:
            return redirect("users:home")

        if not Payment.objects.filter(task=task).exists():
            return redirect("users:home")

        # タスクがNot_Started以外の場合はタスクを削除しない
        if task.status != Task.NOT_STARTED:
            return redirect("users:home")

        task.delete()
        return super().get(request, *args, **kwargs)
