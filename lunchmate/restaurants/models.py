from django.db import models
from datetime import date
from django.utils.translation import gettext as _

from users.models import User


class Restaurant(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="restaurants"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    date = models.DateField(_("Date"), default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "restaurant",
            "date",
        )  # Ensures a restaurant has one menu per day
        ordering = ["-date"]  # Latest menus first

    def __str__(self):
        return f"{self.restaurant.name} Menu - {self.date}"


class MenuItem(models.Model):
    menu = models.ForeignKey(
        "Menu", on_delete=models.CASCADE, related_name="menu_items"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(
        default=True
    )  # If the item is currently available

    def __str__(self):
        return f"{self.name} - {self.price}"
