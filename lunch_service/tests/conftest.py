import datetime
import pytest
from rest_framework.test import APIClient
from apps.authentication.models import Employee
from apps.restaurants.models import Menu, Restaurant


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def employee(db):
    return Employee.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="StrongPass123!",
    )


@pytest.fixture
def admin_employee(db):
    return Employee.objects.create_user(
        username="admin",
        email="admin@example.com",
        password="StrongPass123!",
        is_staff=True,
    )


@pytest.fixture
def auth_client(api_client, employee):
    """Клієнт, авторизований як звичайний співробітник."""
    api_client.force_authenticate(user=employee)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_employee):
    """Клієнт, авторизований як адміністратор."""
    api_client.force_authenticate(user=admin_employee)
    return api_client


@pytest.fixture
def restaurant(db):
    return Restaurant.objects.create(
        name="Puzata Hata", address="Lviv, Sichovykh Strilciv 12"
    )


@pytest.fixture
def today_menu(restaurant):
    return Menu.objects.create(
        restaurant=restaurant,
        date=datetime.date.today(),
        items=[{"name": "Borsch", "price": 80}, {"name": "Varenyky", "price": 100}],
    )
