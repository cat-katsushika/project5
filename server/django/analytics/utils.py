from collections import defaultdict
from datetime import datetime

from tasks.models import Task
from users.models import User


def generate_fine_data(user_id, is_completed):
    dd = defaultdict(int)

    user = User.objects.get(pk=user_id)
    start_date = user.date_joined.date()

    if is_completed:
        tasks = user.task_set.filter(status=Task.DONE)
    else:
        tasks = user.task_set.filter(status=Task.FAILED)

    for task in tasks:
        date = task.updated_at.date()
        date_diff = date - start_date
        dd[date_diff.days] += task.fine

    if 0 not in dd:
        dd[0] = 0

    result = []

    for key, value in dd.items():
        result.append({"x": key, "y": value})

    result.sort(key=lambda x: x["x"])

    today = datetime.now().date()
    today_diff = today - start_date
    today_diff = today_diff.days
    if today_diff not in dd:
        result.append({"x": today_diff, "y": result[-1]["y"]})

    return result
