from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter(name='days_diff')
def days_diff(value, arg):
    """valueとargの日付の差分を日数で返す。"""
    try:
        # valueとargがdatetimeオブジェクトであると仮定
        delta = value - arg.date()
        return str(delta.days )+ "日目"
    except Exception as e:
        return ''
