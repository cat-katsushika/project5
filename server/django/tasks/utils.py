import datetime
import io

import requests
from PIL import Image, ImageDraw, ImageFont

from contacts.models import Contact
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.files import File
from django.db.models import Sum
from tasks.models import Task, TaskOgpImage
from users.models import User


def create_daily_log_text():
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")

    contacts = Contact.objects.all()
    contact_count = contacts.count()
    contact_is_not_resolved_count = contacts.filter(is_resolved=False).count()
    user_count = User.objects.count()
    tasks = Task.objects.all()
    task_in_progress_count = tasks.filter(status=Task.IN_PROGRESS).count()
    task_done_count = tasks.filter(status=Task.DONE).count()
    task_failed_count = tasks.filter(status=Task.FAILED).count()

    # タスクの金額情報
    total_fine_in_progress = tasks.filter(status=Task.IN_PROGRESS).aggregate(total_fine=Sum("fine"))["total_fine"]
    total_fine_done = tasks.filter(status=Task.DONE).aggregate(total_fine=Sum("fine"))["total_fine"]
    total_fine_failed = tasks.filter(status=Task.FAILED).aggregate(total_fine=Sum("fine"))["total_fine"]

    total_fine_in_progress = total_fine_in_progress if total_fine_in_progress else 0
    total_fine_done = total_fine_done if total_fine_done else 0
    total_fine_failed = total_fine_failed if total_fine_failed else 0

    text_list = [
        " ============================= ",
        f"現在時刻:{now}",
        "=== 継続or罰金 定期報告 ===",
        f"問い合わせ数　　　　: {contact_count}",
        f"　未解決問い合わせ数: {contact_is_not_resolved_count}",
        f"ユーザー数　　　　　: {user_count}",
        f"総タスク数　　　　　: {tasks.count()}",
        f"　完了タスク数　　　: {task_done_count}",
        f"　完了タスクの金額　: ¥{total_fine_done:,.0f}",
        f"　進行中タスク数　　: {task_in_progress_count}",
        f"　進行中タスクの金額: ¥{total_fine_in_progress:,.0f}",
        f"　失敗タスク数　　　: {task_failed_count}",
        f"　失敗タスクの金額　: ¥{total_fine_failed:,.0f}",
    ]

    text = "\n".join(text_list)

    return text


def send_message_to_discord(text="メッセージの内容が指定されていません", username="継続or罰金", avatar_url=""):
    # Discordのアイコン画像, べた書きでごめんなさい
    if avatar_url == "":
        avatar_url = "https://keizokuorbakkin.com/static/favicon/favicon.png"

    webhook_url = settings.DISCORD_WEBHOOK_URL

    data = {
        "content": text,
        "username": username,
        "avatar_url": avatar_url,
    }
    requests.post(webhook_url, data=data, timeout=10)


def send_message_to_slack(text="メッセージの内容が指定されていません"):
    token = settings.SLACK_API_TOKEN
    channel = "#継続or罰金"

    # Slack APIのURL
    url = "https://slack.com/api/chat.postMessage"

    # ヘッダとデータを用意
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "channel": channel,
        "text": text,
    }
    # POSTリクエストを送信
    requests.post(url, headers=headers, data=data, timeout=10)


def create_task_detail_ogp_image(task):
    task_ogp_image = TaskOgpImage.objects.filter(task=task).first()
    if task_ogp_image:
        return task_ogp_image

    file_path = finders.find("ogp/task_detail.png")

    # ベースの画像が存在しない場合は白背景の画像を生成
    if file_path:
        base_img = Image.open(file_path)

    else:
        width, height = 1200, 630
        base_img = Image.new("RGB", (width, height), "white")

    font_path = finders.find("fonts/NotoSansJP-Black.ttf")

    created_img = add_centered_text(base_img, task.title, font_path, 64, (32, 32, 32))

    img_byte_arr = io.BytesIO()
    created_img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)  # ストリームの位置をリセット

    # ImageFieldに画像ファイルとして保存
    task_ogp_image = TaskOgpImage(task=task)
    task_ogp_image.image.save(f"{task.id}_ogp.png", File(img_byte_arr, name=f"{task.id}_ogp.png"))
    task_ogp_image.save()

    return task_ogp_image


def add_centered_text(base_img, text, font_path, font_size, font_color):
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(base_img)

    max_lines = 4
    line_spacing = 10

    # 文字がベース画像からはみ出ないように処理
    max_width = base_img.size[0] - 500
    lines = []
    current_line = ""

    for char in text:
        test_line = current_line + char
        text_bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = char

    if current_line:
        lines.append(current_line)

    # 最大行数を超える場合は省略記号を追加
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last_line = lines[-1]
        while (
            draw.textbbox((0, 0), last_line + "...", font=font)[2]
            - draw.textbbox((0, 0), last_line + "...", font=font)[0]
            > max_width
        ):
            last_line = last_line[:-1]
        lines[-1] = last_line + "..."

    # 各行の高さを計算して中央揃えで描画
    line_height = draw.textbbox((0, 0), "あ", font=font)[3] - draw.textbbox((0, 0), "あ", font=font)[1]
    total_text_height = len(lines) * (line_height + line_spacing) - line_spacing
    current_y = (base_img.size[1] - total_text_height) / 2 - 30

    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = ((base_img.size[0] - text_width) / 2) - 150
        draw.text((text_x, current_y), line, fill=font_color, font=font)
        current_y += line_height + line_spacing  # 行の高さにスペースを追加

    return base_img
