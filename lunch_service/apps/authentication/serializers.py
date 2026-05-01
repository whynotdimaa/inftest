from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Employee


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = Employee
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        return Employee.objects.create_user(**validated_data)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "username", "email", "created_at"]
