from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import TaskCreate, TaskDetailView, TodoDoneRedirectView

app_name = "tasks"

urlpatterns = [
    path("create/", TaskCreate.as_view(), name="create-task"),
    path("todo/<uuid:pk>/done/", TodoDoneRedirectView.as_view(), name="todo-done"),
    path("detail/<uuid:pk>/", TaskDetailView.as_view(), name="task-detail"),
]
