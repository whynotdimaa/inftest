import pytest
from rest_framework import status
from django.utils import timezone
from apps.restaurant.models import *

@pytest.mark.django_db
class TestVotingAPI:
    def test_vote_for_menu(self, auth_client, restaurant_factory):
        restaurant = Restaurant.objects.create(name="Lviv Croissants")
        menu = Menu.objects.create(
            restaurant=restaurant,
            date=timezone.now(),
            items = [{'name': 'Croissant', 'price': '100'}]
        )

        response = auth.client.post('/api/voting/', {'menu': menu.id})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['menu'] == menu.id

    def test_double_vote_fails(self, auth_client, restaurant_factory):
        # Перевірка бізнес-правила: один голос на день
        res = Restaurant.objects.create(name="Puzata Hata")
        menu = Menu.objects.create(restaurant=res, date=timezone.now().date(), items=[])

        auth_client.post('/api/voting/', {'menu': menu.id})
        response = auth_client.post('/api/voting/', {'menu': menu.id})

        assert response.status_code == status.HTTP_400_BAD_REQUEST