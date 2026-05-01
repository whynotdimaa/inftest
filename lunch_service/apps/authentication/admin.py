from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = ("email", "username", "is_staff", "created_at")
    ordering = ("-created_at",)