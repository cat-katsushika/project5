from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "username",
        "email",
    )

    ordering = ("username",)


@admin.register(models.LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "attempts",
        "last_attempt",
    )

    ordering = ("user",)
