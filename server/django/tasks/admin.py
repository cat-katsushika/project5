from django.contrib import admin

from . import models


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "fine",
        "id",
    )

    ordering = (
        "status",
        "title",
        "fine",
    )


@admin.register(models.Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "status",
        "date",
        "id",
    )

    ordering = (
        "task",
        "date",
    )


@admin.register(models.RegularExecutionLog)
class RegularExecutionLogAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TaskOgpImage)
class TaskOgpImageAdmin(admin.ModelAdmin):
    pass
