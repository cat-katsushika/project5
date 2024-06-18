import json
import secrets

import requests

from django.conf import settings
from django.db.models import Count
from tasks.models import Task

from .models import EncouragementMessage, Supporter


def get_random_supporter():
    count = Supporter.objects.aggregate(count=Count("id"))["count"]
    if count == 0:
        return Supporter.objects.create(name="テストサポーター", personality="デバッグ中に生成されたサポーターです。")
    random_index = secrets.randbelow(count)  # random.randintの代わりにsecrets.randbelowを使用
    return Supporter.objects.all()[random_index]


def create_encouragement_message(task_id, day_number):
    task = Task.objects.get(pk=task_id)
    supporter = get_random_supporter()

    if EncouragementMessage.objects.filter(task=task, day_number=day_number).exists():
        return
    else:
        if day_number == 0:
            user_state = "5日間の継続を始めようとしている"
        else:
            user_state = f"5日間の継続を目標としており，現在{day_number}日目のタスクを完了した"

        title, message = fetch_encouragement_messages(
            task.title, str(task.user.id), task.user.username, user_state, supporter.name, supporter.personality
        )
        EncouragementMessage.objects.create(
            task=task,
            supporter=supporter,
            title=title,
            message=message,
            day_number=day_number,
        )


def fetch_encouragement_messages(task_name, user_id, user_name, user_state, supporter_name, supporter_personality):
    api_key = settings.DIFY_API_KEY

    url = "https://api.dify.ai/v1/workflows/run"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "inputs": {
            "task_name": task_name,
            "user_name": user_name,
            "user_state": user_state,
            "supporter_name": supporter_name,
            "supporter_personality": supporter_personality,
        },
        "response_mode": "blocking",
        "user": user_id,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=20)
    message = response.json()["data"]["outputs"]["message"]
    title = response.json()["data"]["outputs"]["title"]
    return title, message
