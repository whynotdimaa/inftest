import datetime
from django.db.models import Count, QuerySet


def get_today_result() -> QuerySet:
    """
    Повертає агрегований рейтинг за сьогодні
    """
    from .models import Vote

    return (
        Vote.objects.filter(date=datetime.date.today())
        .values("menu_id", "menu__restaurant__name")
        .annotate(votes=Count("id"))
        .order_by("-votes")
    )
