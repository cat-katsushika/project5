#!/bin/bash
# entrypoint.sh

# データベースマイグレーション
python manage.py migrate

# Djangoサーバーを実行
gunicorn config.wsgi:application --bind 0.0.0.0:8000
