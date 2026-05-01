from django.contrib import admin

from .models import Menu, Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "created_at")
    search_fields = ("name",)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "date", "updated_at")
    list_filter = ("date", "restaurant")
    ordering = ("-date",)
