from django.contrib.auth.models import AbstractUser
from django.db import models

EMPLOYEE = "employee"
RESTAURANT_OWNER = "restaurant_owner"
ADMIN = "admin"


class User(AbstractUser):
    # Inherit fields from AbstractUser: username, first_name, last_name, email, password, etc.

    # Track when the employee was created
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # New field to differentiate between Employee and Restaurant Owner

    ROLE_CHOICES = [
        (EMPLOYEE, "Employee"),
        (RESTAURANT_OWNER, "Restaurant Owner"),
        (ADMIN, "Admin"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=EMPLOYEE)

    def __str__(self):
        return self.username
