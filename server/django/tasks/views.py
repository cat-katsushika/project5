import json
from datetime import datetime, timedelta

import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from payments.models import Payment
from payments.utils import cancel_authorization
from supporters.models import EncouragementMessage
from supporters.utils import create_encouragement_message

from .forms import TaskForm
from .models import RegularExecutionLog, Task, Todo
from .utils import create_daily_log_text, create_task_detail_ogp_image, send_message_to_discord, send_message_to_slack


class TaskFormView(FormView):
    template_name = "tasks/create_task.html"
    form_class = TaskForm
    success_url = reverse_lazy("tasks:confirm_task")

    def form_valid(self, form):
        # フォームのデータをセッションに保存
        self.request.session["task_form_data"] = form.cleaned_data
        return super().form_valid(form)


class TaskConfirmView(TemplateView):
    template_name = "tasks/task_confirm.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context["form_data"] == {}:
            return redirect("tasks:task_form")
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # セッションからフォームデータを取得し、処理を行う
        form_data = request.session.pop("task_form_data", None)
        if form_data is None:
            return redirect("tasks:task_form")

        task = Task.objects.create(
            user=request.user,
            title=form_data["title"],
            fine=form_data["fine"],
        )
        today = task.created_at.date()
        for i in range(1, 6):
            Todo.objects.create(task=task, date=today + timedelta(days=i))

        return redirect("payments:create_checkout_session", pk=task.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_data"] = self.request.session.get("task_form_data", {})
        return context


class TaskDetailView(TemplateView):
    template_name = "tasks/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = get_object_or_404(Task, pk=kwargs["pk"])
        task_ogp_img = create_task_detail_ogp_image(task)
        context["task_ogp_img"] = task_ogp_img
        context["task"] = task
        context["todo_list"] = Todo.objects.filter(task=task).order_by("date")
        context["today"] = datetime.now().date()

        # サポーター関連
        if task.fine >= int(settings.SUPPORTER_MESSAGE_THRESHOLD):
            first_encouragement_message = EncouragementMessage.objects.filter(task=task, day_number=0).first()
            if first_encouragement_message is not None:
                supporter = first_encouragement_message.supporter
                context["supporter"] = supporter
                encouragement_message_list = EncouragementMessage.objects.filter(task=task).order_by("day_number")
                for message in encouragement_message_list:
                    context[f"encouragement_message_day{str(message.day_number)}"] = message

        return context


@login_required
@require_POST
def todo_done_view(request, pk):
    todo = get_object_or_404(Todo, pk=pk)

    # ログインユーザー以外のタスクに対しては403を返す
    if todo.task.user != request.user:
        return HttpResponseForbidden()

    # 当日以外のタスクに対しては403を返す
    if todo.date != datetime.now().date():
        return HttpResponseForbidden()

    if todo.status != Todo.IN_PROGRESS:
        return HttpResponseForbidden()

    todo.status = Todo.DONE
    todo.save()

    completed_todo_count = Todo.objects.filter(task=todo.task, status=Todo.DONE).count()
    if completed_todo_count == 5:
        todo.task.status = Task.DONE
        todo.task.save()

        # オーソリのキャンセル
        cancel_authorization(todo.task.id)

    response_data = {"todo_id": todo.id}

    # # Discordに通知
    # log_message_list = [
    #     " ============================= ",
    #     "順調に継続しているユーザーがいます",
    #     f"ユーザー名: {todo.task.user.username}",
    #     f"タスク名　: {todo.task.title}",
    #     f"罰金額　　: ¥{todo.task.fine:,.0f}",
    #     f"完了日数　: {completed_todo_count}日目",
    # ]
    # log_message = "\n".join(log_message_list)
    # send_message_to_discord(text=log_message, username="継続or罰金 タスクTODO達成検知", avatar_url="")

    # サポーター関連
    if todo.task.fine >= int(settings.SUPPORTER_MESSAGE_THRESHOLD):
        create_encouragement_message(task_id=str(todo.task.id), day_number=completed_todo_count)

    return JsonResponse(response_data)


@csrf_exempt
@require_POST
def regular_execution_view(request):
    data = json.loads(request.body.decode("utf-8"))  # request.bodyはbytes型なのでデコードが必要
    token = data.get("token", "")
    if token != settings.REGULAR_EXECUTION_TOKEN:
        RegularExecutionLog.objects.create(status=RegularExecutionLog.FAILURE, message="invalid token")
        # 1000件を超えたら古いログを削除
        logs = RegularExecutionLog.objects.all()
        if logs.count() > 1000:
            logs.order_by("created_at").first().delete()
        return JsonResponse({"message": "invalid token"}, status=403)

    yesterday = datetime.now().date() - timedelta(days=1)
    yesterday_not_done_todos = Todo.objects.filter(date=yesterday, status=Todo.IN_PROGRESS)
    for todo in yesterday_not_done_todos:
        todo.status = Todo.FAILED
        todo.save()
        todo.task.status = Task.FAILED
        todo.task.save()
        other_todos = Todo.objects.filter(task=todo.task, date__gt=yesterday)
        for other_todo in other_todos:
            other_todo.status = Todo.STOPPED
            other_todo.save()

        # キャプチャの処理
        if todo.task.fine != 0:
            payment = Payment.objects.get(task=todo.task)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe.PaymentIntent.capture(payment.payment_intent_id)

        # # Discordに通知
        # log_message_list = [
        #     " ============================= ",
        #     "継続を続けられなかったユーザーがいます",
        #     f"ユーザー名: {todo.task.user.username}",
        #     f"タスク名　: {todo.task.title}",
        #     f"罰金額　　: ¥{todo.task.fine:,.0f}",
        # ]
        # log_message = "\n".join(log_message_list)
        # send_message_to_discord(text=log_message, username="継続or罰金 継続失敗検知", avatar_url="")

    RegularExecutionLog.objects.create(status=RegularExecutionLog.SUCCESS)
    logs = RegularExecutionLog.objects.all()
    if logs.count() > 1000:
        logs.order_by("created_at").first().delete()

    daily_log_text = create_daily_log_text()
    send_message_to_discord(text=daily_log_text, username="継続or罰金 日次報告", avatar_url="")
    send_message_to_slack(text=daily_log_text)

    return JsonResponse({"message": "success"})
