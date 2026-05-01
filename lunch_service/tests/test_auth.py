import pytest
from rest_framework import status


@pytest.mark.django_db
class TestAuthAPI:
    def test_register_success(self, api_client):
        payload = {
            "username": "new_employee",
            "email": "new@example.com",
            "password": "StrongPass123!",
        }
        response = api_client.post("/api/auth/register/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["username"] == "new_employee"

    def test_login_returns_tokens(self, api_client, employee):
        response = api_client.post(
            "/api/auth/login/",
            {
                "username": employee.username,
                "password": "StrongPass123!",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_me_endpoint_returns_user(self, auth_client, employee):
        response = auth_client.get("/api/auth/me/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == employee.email
