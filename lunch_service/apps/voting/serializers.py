from rest_framework import serializers
from apps.restaurants.models import Menu
from .models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ("id", "menu", "date", "created_at")
        read_only_fields = ("date", "created_at")


    def validate_menu(self,menu):
        import datetime
        if menu.date != datetime.date.today():
            raise serializers.ValidationError("You can only vote for today's menu")
        return menu


#різні формати залежно від версій

class ResultItemV1Serializer(serializers.Serializer):
    restaurant = serializers.CharField(source='menu__restaurant__name')
    votes = serializers.IntegerField()


class ResultItemV2Serializer(serializers.Serializer):
    restaurant = serializers.CharField(source='menu__restaurant__name')
    menu_id = serializers.IntegerField()
    votes = serializers.IntegerField()
    votes = serializers.IntegerField()
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        try:
            menu = Menu.objects.get(pk=obj['menu_id'])
            return menu.items
        except Menu.DoesNotExist:
            return []
