from django.contrib import admin

from . import models


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "is_resolved", "created_at")
    ordering = ("is_resolved", "-created_at",)
