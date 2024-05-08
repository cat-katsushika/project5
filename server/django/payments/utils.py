import stripe

from django.conf import settings
from tasks.models import Task

from .models import Payment


# オーソリをキャンセルする関数
def cancel_authorization(task_id):
    task = Task.objects.get(id=task_id)

    # 罰金が0の場合は何もしない
    if task.fine == 0:
        return

    payment = Payment.objects.get(task=task)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.PaymentIntent.cancel(payment.payment_intent_id)
