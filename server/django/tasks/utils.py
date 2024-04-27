import requests
import datetime
from django.conf import settings
from django.db.models import Sum

from users.models import User
from contacts.models import Contact
from tasks.models import Task

def send_slack_message():
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    contact_count = Contact.objects.count()
    user_count = User.objects.count()
    tasks = Task.objects.all()
    task_in_progress_count = tasks.filter(status=Task.IN_PROGRESS).count()
    task_done_count = tasks.filter(status=Task.DONE).count()
    task_failed_count = tasks.filter(status=Task.FAILED).count()

    # タスクの金額情報
    total_fine_in_progress = tasks.filter(status=Task.IN_PROGRESS).aggregate(total_fine=Sum("fine"))[ "total_fine"]
    total_fine_done = tasks.filter(status=Task.DONE).aggregate(total_fine=Sum("fine"))["total_fine"]
    total_fine_failed = tasks.filter(status=Task.FAILED).aggregate(total_fine=Sum("fine"))["total_fine"]

    total_fine_in_progress = total_fine_in_progress if total_fine_in_progress else 0
    total_fine_done = total_fine_done if total_fine_done else 0
    total_fine_failed = total_fine_failed if total_fine_failed else 0

    token = settings.SLACK_API_TOKEN
    channel = '#継続or罰金'
    text_list = [
        f' ============================= ',
        f'現在時刻:{now}',
        f'=== 継続or罰金 定期報告 ===',
        f'問い合わせ数　　　　: {contact_count}',
        f'ユーザー数　　　　　: {user_count}',
        f'総タスク数　　　　　: {tasks.count()}',
        f'　完了タスク数　　　: {task_done_count}',
        f'　完了タスクの金額　: ¥{total_fine_done:,.0f}',
        f'　進行中タスク数　　: {task_in_progress_count}',
        f'　進行中タスクの金額: ¥{total_fine_in_progress:,.0f}',
        f'　失敗タスク数　　　: {task_failed_count}',
        f'　失敗タスクの金額　: ¥{total_fine_failed:,.0f}',
    ]

    text = '\n'.join(text_list)


    # Slack APIのURL
    url = 'https://slack.com/api/chat.postMessage'

    # ヘッダとデータを用意
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'channel': channel,
        'text': text,
    }

    # POSTリクエストを送信
    try:
        requests.post(url, headers=headers, data=data, timeout=10)
    except:
        pass
