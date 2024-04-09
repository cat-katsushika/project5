from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "payment_intent_id",
        "checkout_session_id",
    )

    ordering = ("payment_intent_id",)

    search_fields = ("payment_intent_id",)
