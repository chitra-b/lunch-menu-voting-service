from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone

from restaurants.models import Restaurant, Menu, MenuItem
from votings.models import Vote
from users.models import User

test_employee_data = {
    "username": "test_emp",
    "password": "password123",
    "email": "test_emp@example.com",
    "role": "employee",
}
emp_login = {
    "username": test_employee_data["username"],
    "password": test_employee_data["password"],
}
test_restaurant_owner_data = {
    "username": "test_res_owner",
    "password": "password123",
    "email": "test_res_owner@example.com",
    "role": "restaurant_owner",
}
restaurant_owner_login = {
    "username": test_restaurant_owner_data["username"],
    "password": test_restaurant_owner_data["password"],
}
test_res = {"name": "Test Res", "description": "Test Res"}
test_res1 = {"name": "Test Res", "description": "Test Res"}
test_res2 = {"name": "Test Res", "description": "Test Res"}
test_res3 = {"name": "Test Res", "description": "Test Res"}

menu = {"date": timezone.now().date()}
menu1 = {"date": timezone.now().date()}
menu2 = {"date": timezone.now().date()}
menu3 = {"date": timezone.now().date()}
items = [
    {"name": "one", "price": 5.99},
    {"name": "two", "price": 4.50},
    {"name": "three", "price": 8.99},
]


class VotingTest(APITestCase):
    def setUp(self):
        # Create a user
        self.employee = User.objects.create_user(**test_employee_data)
        self.restaurant_owner = User.objects.create_user(**test_restaurant_owner_data)
        self.login_url = reverse("token_obtain_pair")
        emp_response = self.client.post(
            self.login_url,
            emp_login,
        )
        self.emp_access_token = emp_response.data["access"]
        # restaurant_owner_response = self.client.post(
        #     self.login_url,
        #     restaurant_owner_login,
        # )
        # self.restaurant_owner_access_token = restaurant_owner_response.data["access"]
        # self.restaurant_owner_refresh_token = restaurant_owner_response.data["refresh"]

        # Create a restaurant and menu
        test_res["owner"] = self.restaurant_owner
        test_res1["owner"] = self.restaurant_owner
        test_res2["owner"] = self.restaurant_owner
        test_res3["owner"] = self.restaurant_owner
        self.restaurant = Restaurant.objects.create(**test_res)
        self.restaurant1 = Restaurant.objects.create(**test_res1)
        self.restaurant2 = Restaurant.objects.create(**test_res2)
        self.restaurant3 = Restaurant.objects.create(**test_res3)
        menu["restaurant"] = self.restaurant
        menu1["restaurant"] = self.restaurant1
        menu2["restaurant"] = self.restaurant2
        menu3["restaurant"] = self.restaurant3
        self.menu = Menu.objects.create(**menu)
        self.menu1 = Menu.objects.create(**menu1)
        self.menu2 = Menu.objects.create(**menu2)
        self.menu3 = Menu.objects.create(**menu3)
        for item_data in items:
            MenuItem.objects.create(menu=self.menu, **item_data)
            MenuItem.objects.create(menu=self.menu1, **item_data)
            MenuItem.objects.create(menu=self.menu2, **item_data)
            MenuItem.objects.create(menu=self.menu3, **item_data)

        self.vote_url = reverse("votes-list")

        self.old_api_headers = {"HTTP_API-Version": "1.0"}
        self.new_api_headers = {"HTTP_API-Version": "2.0"}

    def test_old_api_single_vote(self):
        vote_data = {"menu": self.menu.id}
        response = self.client.post(
            self.vote_url,
            vote_data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.emp_access_token}",
            **self.old_api_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ensure that only one vote is cast for the menu
        self.assertEqual(Vote.objects.count(), 1)
        vote = Vote.objects.first()
        self.assertEqual(vote.user, self.employee)
        self.assertEqual(vote.menu, self.menu)
        self.assertEqual(vote.points, 3)

    def test_new_api_multiple_votes_with_points(self):
        # Voting for top three menus (new version)
        vote_data = {
            "votes": [
                {"menu": self.menu1.id, "rank": 3},
                {"menu": self.menu2.id, "rank": 2},
                {"menu": self.menu3.id, "rank": 1},
            ]
        }
        response = self.client.post(
            self.vote_url,
            vote_data,
            format="json",
            HTTP_AUTHORIZATION=f"Bearer {self.emp_access_token}",
            **self.new_api_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vote.objects.count(), 3)

        # Validate votes and points
        vote1 = Vote.objects.get(menu=self.menu1)
        vote2 = Vote.objects.get(menu=self.menu2)
        vote3 = Vote.objects.get(menu=self.menu3)

        self.assertEqual(vote1.user, self.employee)
        self.assertEqual(vote1.points, 1)

        self.assertEqual(vote2.user, self.employee)
        self.assertEqual(vote2.points, 2)

        self.assertEqual(vote3.user, self.employee)
        self.assertEqual(vote3.points, 3)

    def test_current_day_results(self):
        """Test if the current day's results are returned correctly for an authenticated user."""

        # Create users
        self.user1 = User.objects.create_user(username="user1", password="testpass123")
        self.user2 = User.objects.create_user(username="user2", password="testpass123")
        self.user3 = User.objects.create_user(username="user3", password="testpass123")

        # Create votes
        Vote.objects.create(user=self.user1, menu=self.menu1, rank=3, points=1)
        Vote.objects.create(user=self.user1, menu=self.menu2, rank=2, points=2)
        Vote.objects.create(user=self.user1, menu=self.menu3, rank=1, points=3)

        Vote.objects.create(user=self.user2, menu=self.menu1, rank=2, points=2)
        Vote.objects.create(user=self.user2, menu=self.menu3, rank=1, points=3)

        Vote.objects.create(user=self.user3, menu=self.menu1, rank=1, points=3)
        Vote.objects.create(user=self.user3, menu=self.menu2, rank=2, points=2)
        Vote.objects.create(user=self.user3, menu=self.menu3, rank=3, points=1)

        # Get current day results
        url = reverse(
            "votes-current-day-results"
        )  # Make sure this matches your URL config
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=f"Bearer {self.emp_access_token}",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate the points for each menu
        for menu_result in response.data["results"]:
            menu_id = menu_result["menu_id"]
            if menu_id == self.menu1.id:
                self.assertEqual(
                    menu_result["total_points"], 6
                )  # 1 pt (user1) + 2 pt (user2) + 3 pts (user3)
            elif menu_id == self.menu2.id:
                self.assertEqual(
                    menu_result["total_points"], 4
                )  # 2 pt (user1) + 2 pt (user3)
            elif menu_id == self.menu3.id:
                self.assertEqual(
                    menu_result["total_points"], 7
                )  # 3 pt (user1) + 3 pt (user2) + 1 pt (user3)
