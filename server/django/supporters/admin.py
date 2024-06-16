from django.contrib import admin
from django.utils.html import format_html

from . import models


@admin.register(models.Supporter)
class SupporterAdmin(admin.ModelAdmin):
    list_display = ("name", "personality", "avatar_tag")

    def avatar_tag(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" />', obj.avatar.url)
        return "-"

    avatar_tag.short_description = "Avatar"
    avatar_tag.allow_tags = True


@admin.register(models.EncouragementMessage)
class EncouragementMessageAdmin(admin.ModelAdmin):
    pass
