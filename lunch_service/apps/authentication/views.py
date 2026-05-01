from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny

from .models import Employee
from .serializers import EmployeeSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    # Створення нового Employee

    queryset = Employee.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class MyView(generics.RetrieveAPIView):
    # Дані поточного employee

    serializer_class = EmployeeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
