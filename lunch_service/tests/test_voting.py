import pytest
from rest_framework import status
from django.utils import timezone
from apps.restaurants.models import *
import datetime
import pytest
from apps.voting.models import Vote

@pytest.mark.django_db
class TestVotingAPI:
    def test_vote_for_menu(self, auth_client, today_menu):
        response = auth_client.post("/api/voting/", {"menu": today_menu.id})
        assert response.status_code == status.HTTP_201_CREATED

    def test_double_vote_fails(self, auth_client, today_menu):
        auth_client.post("/api/voting/", {"menu": today_menu.id})
        response = auth_client.post("/api/voting/", {"menu": today_menu.id})

        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT]

    def test_vote_success(self, auth_client, today_menu):
        response = auth_client.post("/api/voting/", {"menu": today_menu.id})
        assert response.status_code == status.HTTP_201_CREATED

    def test_results_v1_format(self, auth_client, today_menu, employee):
        Vote.objects.create(employee=employee, menu=today_menu, date=datetime.date.today())

        response = auth_client.get("/api/voting/results/today/", HTTP_BUILD_VERSION="1")
        assert response.status_code == status.HTTP_200_OK
        assert "items" not in response.data[0]

    def test_results_v2_format(self, auth_client, today_menu, employee):
        Vote.objects.create(employee=employee, menu=today_menu, date=datetime.date.today())

        response = auth_client.get("/api/voting/results/today/", HTTP_BUILD_VERSION="2")
        assert response.status_code == status.HTTP_200_OK
        assert "items" in response.data[0]