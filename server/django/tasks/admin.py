from django.contrib import admin

from . import models


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Todo)
class TodoAdmin(admin.ModelAdmin):
    pass
