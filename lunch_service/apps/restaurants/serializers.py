from rest_framework import serializers
from .models import Menu, Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'created_at')


class MenuSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)

    class Meta:
        model = Menu
        fields = ('id', 'restaurant', 'restaurant_name', 'date', 'items', 'updated_at')

    def validate_items(self, value):
        #item має бути не порожній
        if not isinstance(value, list) or not value:
            raise serializers.ValidationError('Please enter a valid list')
        for item in value:
            if not instance(item, dict) or 'name' not in item:
                raise serializers.ValidationError('Each item must be an object with at least a "name" field')
        return value