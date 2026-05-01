from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=200, verbose_name="Restaurant Name")
    address = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()
    items = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("restaurant", "date")
        ordering = ("-date",)

    def __str__(self):
        return f"Menu for {self.restaurant} on {self.date}"
