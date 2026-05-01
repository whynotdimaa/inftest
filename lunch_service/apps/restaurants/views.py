import datetime
from rest_framework import generics, permissions

from .models import Menu, Restaurant
from .serializers import MenuSerializer, RestaurantSerializer


class RestaurantListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/restaurants/         — список всіх ресторанів
    POST /api/restaurants/         — створити ресторан (тільки staff)
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE /api/restaurants/<id>/"""

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MenuUploadView(generics.CreateAPIView):
    """
    POST /api/restaurants/<restaurant_id>/menu/
    Ресторан завантажує меню на день. Якщо меню на цю дату вже є — оновлює.
    """

    serializer_class = MenuSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer(self, *args, **kwargs):
        # Додаємо ID ресторану з URL до даних, які йдуть на валідацію
        if "data" in kwargs:
            data = kwargs["data"].copy()
            data["restaurant"] = self.kwargs.get("restaurant_id")
            kwargs["data"] = data
        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        restaurant = generics.get_object_or_404(
            Restaurant, pk=self.kwargs["restaurant_id"]
        )
        date = serializer.validated_data.get("date", datetime.date.today())

        menu, _ = Menu.objects.update_or_create(
            restaurant=restaurant,
            date=date,
            defaults={"items": serializer.validated_data["items"]},
        )
        serializer.instance = menu


class TodayMenuListView(generics.ListAPIView):
    """GET /api/restaurants/menu/today/ — меню всіх ресторанів на сьогодні."""

    serializer_class = MenuSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Menu.objects.filter(date=datetime.date.today()).select_related(
            "restaurant"
        )
