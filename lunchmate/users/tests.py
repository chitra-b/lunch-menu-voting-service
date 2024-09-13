from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User

test_user_data = {
    "username": "testuser",
    "password": "password123",
    "email": "testuser@example.com",
}
test_user_login = {
    "username": test_user_data["username"],
    "password": test_user_data["password"],
}

user_signup_employee_data = {
    "username": "emp",
    "password": "password123",
    "email": "emp@example.com",
    "role": "employee",
}
user_signup_restaurant_owner_data = {
    "username": "res-owner",
    "password": "password123",
    "email": "res-owner@example.com",
    "role": "restaurant_owner",
}
change_password_data = {
    "old_password": test_user_data["password"],
    "new_password": "newpassword123",
}


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(**test_user_data)
        self.login_url = reverse("token_obtain_pair")

    def test_user_signup_employee(self):
        url = reverse("users-list")
        response = self.client.post(url, user_signup_employee_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_signup_restaurant_owner(self):
        url = reverse("users-list")
        response = self.client.post(url, user_signup_restaurant_owner_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        response = self.client.post(
            self.login_url,
            test_user_login,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # Check for JWT token

    def test_logout(self):
        # Pass the refresh token for logout (blacklisting)
        response = self.client.post(
            self.login_url,
            test_user_login,
        )
        self.access_token = response.data["access"]
        self.refresh_token = response.data["refresh"]
        self.logout_url = reverse("logout")
        response = self.client.post(
            self.logout_url,
            {"refresh_token": self.refresh_token},
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        response = self.client.post(
            self.login_url,
            test_user_login,
        )
        self.access_token = response.data["access"]
        self.refresh_token = response.data["refresh"]
        self.change_password_url = reverse("change-password")
        response = self.client.put(
            self.change_password_url,
            change_password_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test login with new password
        self.client.logout()
        login_response = self.client.post(
            self.login_url,
            {
                "username": test_user_data["username"],
                "password": change_password_data["new_password"],
            },
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
