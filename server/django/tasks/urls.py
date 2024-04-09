from django.urls import path

from .views import TaskConfirmView, TaskDetailView, TaskFormView, regular_execution_view, todo_done_view

app_name = "tasks"

urlpatterns = [
    path("todo/<uuid:pk>/done/", todo_done_view, name="todo_done"),
    path("detail/<uuid:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("form/", TaskFormView.as_view(), name="task_form"),
    path("confirm/", TaskConfirmView.as_view(), name="confirm_task"),
    path("regular_execution/", regular_execution_view, name="regular_execution"),
]
