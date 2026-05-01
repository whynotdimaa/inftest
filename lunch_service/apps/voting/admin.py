from django.contrib import admin

from .models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("id", "menu", "employee", "created_at")
    list_filter = ("date",)
    ordering = ("-date",)
