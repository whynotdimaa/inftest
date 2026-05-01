import datetime
import pytest
from rest_framework import status


@pytest.mark.django_db
class TestRestaurantAPI:
    def test_create_restaurant_as_admin(self, admin_client):
        response = admin_client.post(
            "/api/restaurants/", {"name": "Kulykivska", "address": "Lviv, 1"}
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_restaurant_as_user_fails(self, auth_client):
        response = auth_client.post("/api/restaurants/", {"name": "Forbidden"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_upload_menu_as_admin(self, admin_client, restaurant):
        payload = {
            "date": datetime.date.today().isoformat(),
            "items": [{"name": "Steak", "price": 200}],
        }
        response = admin_client.post(
            f"/api/restaurants/{restaurant.id}/menu/", payload, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_today_menus(self, auth_client, today_menu):
        response = auth_client.get("/api/restaurants/menu/today/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
