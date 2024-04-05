from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView

from .forms import TaskForm
from .models import Task, Todo


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/create_task.html"

    def form_valid(self, form):
        form.instance.user = self.request.user  # 作成者を現在のユーザーに設定
        response = super().form_valid(form)

        today = datetime.now().date()
        for i in range(1, 8):
            Todo.objects.create(task=self.object, date=today + timedelta(days=i))
        return response

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy("users:profile", kwargs={"pk": user.id})


class TodoDoneRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=kwargs["pk"])
        todo.status = Todo.DONE
        todo.save()
        user = self.request.user
        return reverse_lazy("users:profile", kwargs={"pk": user.id})


class TaskDetailView(TemplateView):
    template_name = "tasks/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=kwargs["pk"])
        context["task"] = task
        context["todo_list"] = Todo.objects.filter(task=task).order_by("date")
        return context
