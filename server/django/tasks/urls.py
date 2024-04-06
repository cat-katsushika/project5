from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import TaskDetailView, TodoDoneRedirectView, TaskFormView, TaskConfirmView

app_name = "tasks"

urlpatterns = [
    path("todo/<uuid:pk>/done/", TodoDoneRedirectView.as_view(), name="todo-done"),
    path("detail/<uuid:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path('form/', TaskFormView.as_view(), name='task_form'),
    path('confirm/', TaskConfirmView.as_view(), name='confirm_task'),
]
