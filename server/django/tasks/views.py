from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.shortcuts import redirect

from .forms import TaskForm
from .models import Task, Todo

    
class TaskFormView(FormView):
    template_name = 'tasks/create_task.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:confirm_task')

    def form_valid(self, form):
        # フォームのデータをセッションに保存
        self.request.session['task_form_data'] = form.cleaned_data
        return super().form_valid(form)

class TaskConfirmView(TemplateView):
    template_name = 'tasks/task_confirm.html'

    def post(self, request, *args, **kwargs):
        # セッションからフォームデータを取得し、処理を行う
        form_data = request.session.pop('task_form_data', None)
        if form_data is None:
            return redirect('tasks:task_form')
        
        task = Task.objects.create(
            user=request.user,
            title=form_data['title'],
            fine=form_data['fine'],
        )
        today = task.created_at.date()
        for i in range(1, 8):
            Todo.objects.create(task=task, date=today + timedelta(days=i))
        
        user = self.request.user
        return redirect("users:profile", pk=user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_data'] = self.request.session.get('task_form_data', {})
        return context


class TodoDoneRedirectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=kwargs["pk"])
        todo.status = Todo.DONE
        todo.save()
        
        completed_todo_count = Todo.objects.filter(task=todo.task, status=Todo.DONE).count()
        if completed_todo_count == 7:
            todo.task.status = Task.DONE
            todo.task.save()
        
        
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
