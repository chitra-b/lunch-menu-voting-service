from rest_framework.serializers import ModelSerializer, ReadOnlyField

from restaurants.models import Restaurant, Menu, MenuItem


class RestaurantSerializer(ModelSerializer):
    owner = ReadOnlyField(source="owner.username")

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "owner",
            "name",
            "description",
            "phone_number",
            "created_at",
            "updated_at",
        ]


class MenuItemSerializer(ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "name", "description", "price", "is_available"]


class MenuSerializer(ModelSerializer):
    menu_items = MenuItemSerializer(many=True)

    class Meta:
        model = Menu
        fields = ["id", "restaurant", "date", "menu_items"]

    def create(self, validated_data):
        # Create menu along with associated menu items
        menu_items_data = validated_data.pop("menu_items")
        menu = Menu.objects.create(**validated_data)
        for item_data in menu_items_data:
            MenuItem.objects.create(menu=menu, **item_data)
        return menu

    def update(self, instance, validated_data):
        # Update menu and menu items
        menu_items_data = validated_data.pop("menu_items", None)
        instance.date = validated_data.get("date", instance.date)
        instance.save()

        # Clear existing menu items
        if menu_items_data is not None:
            instance.menu_items.all().delete()
            for item_data in menu_items_data:
                MenuItem.objects.create(menu=instance, **item_data)

        return instance
