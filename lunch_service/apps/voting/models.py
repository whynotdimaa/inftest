from django.db import models
from django.conf import settings
from apps.restaurants.models import Menu

class Vote(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.employee} -> {self.menu.restaurant.name} ({self.date})"
