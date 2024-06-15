from datetime import datetime, timedelta

import pyotp
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount

from django.conf import settings
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.edit import UpdateView
from tasks.models import Task, Todo

from .forms import AdminOneTimePasswordForm, UsernameChangeForm
from .utils import generate_random_string, is_unique_username

User = get_user_model()


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

        context["today"] = datetime.now().date()
        context["tomorrow"] = datetime.now().date() + timedelta(days=1)

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

    # 削除ユーザー用のユーザー名に変更
    unique = False
    while not unique:
        random_string = generate_random_string()
        new_username = f"D_{random_string}"
        if is_unique_username(new_username):
            user.username = new_username
            user.is_active = False
            user.save()
            unique = True

    tasks = Task.objects.filter(user=user)
    for task in tasks:
        task.title = "削除されたユーザーのタスク"
        task.save()

    user.email = ""
    user.first_name = ""
    user.last_name = ""
    user.save()
    SocialAccount.objects.filter(user=user).delete()
    EmailAddress.objects.filter(user=user).delete()

    # ユーザーをログアウトさせる
    logout(request)

    # ホームページなど、適切なページにリダイレクト
    return redirect("users:home")


def custom_admin_auth_view(request):
    """
    Adminページにワンタイムパスワードを設定するためのカスタム認証ビュー
    """
    if settings.DEBUG:
        # DEBUGモードの場合はカスタム認証をスキップ
        request.session["custom_admin_auth"] = True
        return redirect("/admin/KOgEdTnMXbsDJa8jK347oaVqVzbshgIfhOWBjim9uEA5RfsEpl/")

    if request.method == "POST":
        form = AdminOneTimePasswordForm(request.POST)

        if form.is_valid():
            one_time_password = form.cleaned_data.get("one_time_password")

            # ワンタイムパスワードの検証
            if pyotp.TOTP(settings.ONE_TIME_PASSWORD_SECRET).verify(one_time_password):
                request.session["custom_admin_auth"] = True
                return redirect("/admin/KOgEdTnMXbsDJa8jK347oaVqVzbshgIfhOWBjim9uEA5RfsEpl/")
            else:
                form.add_error(None, "ワンタイムパスワードが正しくありません")
    else:
        form = AdminOneTimePasswordForm()
        request.session["custom_admin_auth"] = False

    return render(request, "users/custom_admin_auth.html", {"form": form})
