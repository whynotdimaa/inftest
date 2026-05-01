from django.urls import path

from .views import MenuUploadView, RestaurantDetailView, RestaurantListCreateView, TodayMenuListView

urlpatterns = [
    path("", RestaurantListCreateView.as_view(), name="restaurant-list"),
    path("<int:pk>/", RestaurantDetailView.as_view(), name="restaurant-detail"),
    path("<int:restaurant_id>/menu/", MenuUploadView.as_view(), name="menu-upload"),
    path("menu/today/", TodayMenuListView.as_view(), name="menu-today"),
]