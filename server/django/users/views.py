from datetime import datetime, timedelta

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.edit import UpdateView
from tasks.models import Task, Todo

from .forms import SignUpForm, UsernameChangeForm

User = get_user_model()


class SignUpView(CreateView):
    template_name = "users/signup.html"
    form_class = SignUpForm

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response

    def get_success_url(self):
        # 処理の順番的に，直接プロファイルにリダイレクトできないため，ワンクッション置いている．
        # form_validでsuper().form_validを最初に呼ぶと，get_success_urlでrequest.userが取得できない．
        # form_validでsuper().form_validを最後に呼ぶと，ログインができなくなる．
        return reverse_lazy("users:profile_redirect")


class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        # ユーザーのUUIDを使ってプロフィールページのURLを生成
        return reverse_lazy("users:profile", kwargs={"pk": user.id})


class HomePageView(TemplateView):
    template_name = "users/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_fine_in_progress = Task.objects.filter(status=Task.IN_PROGRESS).aggregate(total_fine=Sum("fine"))[
            "total_fine"
        ]
        total_fine_done = Task.objects.filter(status=Task.DONE).aggregate(total_fine=Sum("fine"))["total_fine"]
        total_fine_failed = Task.objects.filter(status=Task.FAILED).aggregate(total_fine=Sum("fine"))["total_fine"]

        total_fine_in_progress = total_fine_in_progress if total_fine_in_progress else 0
        total_fine_done = total_fine_done if total_fine_done else 0
        total_fine_failed = total_fine_failed if total_fine_failed else 0

        formatted_total_fine_in_progress = f"¥{total_fine_in_progress:,.0f}"
        formatted_total_fine_done = f"¥{total_fine_done:,.0f}"
        formatted_total_fine_failed = f"¥{total_fine_failed:,.0f}"

        context["total_fine_in_progress"] = formatted_total_fine_in_progress
        context["total_fine_done"] = formatted_total_fine_done
        context["total_fine_failed"] = formatted_total_fine_failed

        # statusがIN_PROGRESSまたはFAILEDのタスクを取得

        recent_tasks = Task.objects.exclude(status=Task.NOT_STARTED).order_by("-created_at")[:5]
        high_fine_tasks = Task.objects.exclude(status=Task.NOT_STARTED).order_by("-fine")[:5]
        completed_tasks = Task.objects.filter(status=Task.DONE).order_by("-updated_at")[:5]
        context["recent_tasks"] = recent_tasks
        context["high_fine_tasks"] = high_fine_tasks
        context["completed_tasks"] = completed_tasks

        return context


class UserProfileView(TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = User.objects.get(pk=self.kwargs["pk"])
        context["todo_list_today"] = (
            Todo.objects.filter(task__user=context["profile"], date=datetime.now().date())
            .exclude(status=Todo.NOT_STARTED)
            .exclude(status=Todo.FAILED)
            .exclude(status=Todo.STOPPED)
        )
        context["todo_list_tomorrow"] = (
            Todo.objects.filter(
                task__user=context["profile"],
                date=datetime.now().date() + timedelta(days=1),
            )
            .exclude(status=Todo.NOT_STARTED)
            .exclude(status=Todo.FAILED)
            .exclude(status=Todo.STOPPED)
        )

        total_fine_in_progress = Task.objects.filter(user=context["profile"], status=Task.IN_PROGRESS).aggregate(
            total_fine=Sum("fine")
        )["total_fine"]
        total_fine_done = Task.objects.filter(user=context["profile"], status=Task.DONE).aggregate(
            total_fine=Sum("fine")
        )["total_fine"]
        total_fine_failed = Task.objects.filter(user=context["profile"], status=Task.FAILED).aggregate(
            total_fine=Sum("fine")
        )["total_fine"]

        context["total_fine_in_progress"] = total_fine_in_progress if total_fine_in_progress else 0
        context["total_fine_done"] = total_fine_done if total_fine_done else 0
        context["total_fine_failed"] = total_fine_failed if total_fine_failed else 0

        done_tasks = Task.objects.filter(user=context["profile"], status=Task.DONE)
        in_progress_tasks = Task.objects.filter(user=context["profile"], status=Task.IN_PROGRESS)
        failed_tasks = Task.objects.filter(user=context["profile"], status=Task.FAILED)
        context["done_tasks"] = done_tasks
        context["in_progress_tasks"] = in_progress_tasks
        context["failed_tasks"] = failed_tasks

        return context


class UserProfileRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        return reverse_lazy("users:profile", kwargs={"pk": user.id})


class UsernameChangeView(LoginRequiredMixin, UpdateView):
    form_class = UsernameChangeForm
    template_name = "users/username_change_form.html"

    def get_object(self):
        # ログインしているユーザーのオブジェクトを返す
        return self.request.user

    def get_success_url(self):
        user = self.request.user
        return reverse_lazy("users:profile", kwargs={"pk": user.id})


class UserDeactivateConfirmView(TemplateView):
    template_name = "users/user_deactivate_confirm.html"


@login_required
def deactivate_account_view(request):
    user = request.user
    user.username = "削除されたユーザー" + "-" + str(user.id)
    user.is_active = False
    user.save()

    tasks = Task.objects.filter(user=user)
    for task in tasks:
        task.title = "削除されたユーザーのタスク"
        task.save()

    # ユーザーをログアウトさせる
    logout(request)

    # ホームページなど、適切なページにリダイレクト
    return redirect("users:home")
