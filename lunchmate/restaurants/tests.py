from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone

from restaurants.models import Restaurant, Menu, MenuItem
from users.models import User

# Data set up

owner_data = {
    "username": "test_owner",
    "password": "ownerpassword",
    "role": "restaurant_owner",
}
restaurant_data_1 = {
    "name": "Test Restaurant 1",
    "description": "Test Restaurant description 1",
}
restaurant_data_2 = {
    "name": "Test Restaurant 2",
    "description": "Test Restaurant description 2",
}
menu_data = {
    "menu_items": [
        {"name": "Burger", "price": 5.99},
        {"name": "Salad", "price": 4.50},
        {"name": "Pizza", "price": 8.99},
    ],
}
today_menu_data = {"date": timezone.now().date()}
today_menu_items = [
    {"name": "Veg Soup", "price": 5.99},
    {"name": "Veg Grill", "price": 4.50},
    {"name": "Veg Sandwich", "price": 8.99},
]


class RestaurantCreateWithOwnerTest(APITestCase):
    def setUp(self):
        # Create a user who will be the owner & Login
        self.owner = User.objects.create_user(**owner_data)
        self.login_url = reverse("token_obtain_pair")
        response = self.client.post(
            self.login_url,
            {"username": owner_data["username"], "password": owner_data["password"]},
        )
        self.access_token = response.data["access"]
        self.refresh_token = response.data["refresh"]

        # Restaurant data set up
        self.restaurant_url = reverse("restaurants-list")
        restaurant_data_1["owner"] = self.owner.id
        self.restaurant_data = restaurant_data_1

        #  Test restaurant create
        restaurant_data_2["owner"] = self.owner
        self.restaurant = Restaurant.objects.create(**restaurant_data_2)

        # Current day menu set up
        self.daily_menu_url = reverse("menus-current-day-menu")

    def test_create_restaurant_with_owner(self):
        response = self.client.post(
            self.restaurant_url,
            self.restaurant_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        restaurant = Restaurant.objects.get(id=response.data["id"])
        self.assertEqual(restaurant.name, restaurant_data_1["name"])
        self.assertEqual(restaurant.owner, self.owner)

    def test_create_daily_menu_with_items(self):
        self.menu_url = reverse("menus-list")
        menu_data["restaurant"] = self.restaurant.id
        response = self.client.post(
            self.menu_url,
            menu_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), len(menu_data["menu_items"]))

        # Validate the menu
        menu = Menu.objects.get(id=response.data["id"])
        self.assertEqual(menu.restaurant, self.restaurant)

        # Validate the associated menu items
        items = MenuItem.objects.filter(menu=menu)
        self.assertEqual(items.count(), len(menu_data["menu_items"]))
        for each_menu in menu_data["menu_items"]:
            self.assertTrue(items.filter(name=each_menu["name"]).exists())

    def test_get_current_day_menu(self):
        today_menu_data["restaurant"] = self.restaurant
        self.today_menu = Menu.objects.create(**today_menu_data)
        for item_data in today_menu_items:
            MenuItem.objects.create(menu=self.today_menu, **item_data)
        response = self.client.get(
            self.daily_menu_url,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["restaurant"], self.restaurant.id)
        self.assertEqual(response.data[0]["date"], str(timezone.now().date()))
