from datetime import datetime, timedelta

from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.views.generic.base import TemplateView
from tasks.models import Task, Todo

from .forms import SignUpForm

User = get_user_model()


class SignUpView(CreateView):
    template_name = "users/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        # ユーザーのUUIDを使ってプロフィールページのURLを生成
        return reverse_lazy("users:profile", kwargs={"pk": user.id})


class HomePageView(TemplateView):
    template_name = "users/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserProfileView(TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = User.objects.get(pk=self.kwargs["pk"])
        context["todo_list_today"] = Todo.objects.filter(
            task__user=context["profile"], date=datetime.now().date()
        )
        context["todo_list_tomorrow"] = Todo.objects.filter(
            task__user=context["profile"],
            date=datetime.now().date() + timedelta(days=1),
        )
        
        
        total_fine_in_progress = Task.objects.filter(
            user=context["profile"], status=Task.IN_PROGRESS
        ).aggregate(total_fine=Sum("fine"))["total_fine"]
        total_fine_done = Task.objects.filter(
            user=context["profile"], status=Task.DONE
        ).aggregate(total_fine=Sum("fine"))["total_fine"]
        total_fine_failed = Task.objects.filter(
            user=context["profile"], status=Task.FAILED
        ).aggregate(total_fine=Sum("fine"))["total_fine"]
        
        context["total_fine_in_progress"] = total_fine_in_progress if total_fine_in_progress else 0
        context["total_fine_done"] = total_fine_done if total_fine_done else 0
        context["total_fine_failed"] = total_fine_failed if total_fine_failed else 0
        return context
