from datetime import datetime
from django.utils import timezone


def time_delta_seconds(start: datetime, finish: datetime):
    delta = finish - start
    return int(delta.total_seconds())

def total_seconds_since(start: datetime):
    now = timezone.now()
    return time_delta_seconds(start, now)