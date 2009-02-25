from django import template
from django.utils.timesince import timesince
from datetime import datetime, timedelta
from django_gitweb.utils import pygmentize

register = template.Library()

@register.filter
def time2datetime(value):
    try:
        return datetime(*value[0:6])
    except:
        return None

@register.filter
def conditional_timesince(value, max_age_days=7, fmt='%Y-%m-%d'):
    try:
        if value >= datetime.now() - timedelta(days=max_age_days):
            return timesince(value)
        else:
            return value.strftime(fmt)
    except:
        return value

@register.filter
def pygmentize_diff(blob):
    try:
        return pygmentize('diff', blob)
    except:
        return blob
