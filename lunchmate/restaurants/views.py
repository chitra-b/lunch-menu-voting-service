# views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.decorators import action
from django.utils import timezone

from restaurants.models import Restaurant, Menu, MenuItem
from restaurants.serializers import (
    RestaurantSerializer,
    MenuSerializer,
    MenuItemSerializer,
)
from users.permissions import IsRestaurantOwner


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_permissions(self):
        """
        Set different permissions for different actions.
        """
        if self.action == "list":
            # Anyone can view the list of restaurants
            permission_classes = [IsAuthenticated()]
        else:
            # Only owners can create/edit/delete restaurants
            permission_classes = [IsRestaurantOwner()]

        return permission_classes

    def perform_create(self, serializer):
        # Set the restaurant owner to the authenticated user when creating a new restaurant
        serializer.save(owner=self.request.user)


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"], url_path="current-day-menu")
    def current_day_menu(self, request):
        # Get the current date
        current_date = timezone.now().date()
        # Filter menus by today's date
        menus = Menu.objects.filter(date=current_date)
        serializer = self.get_serializer(menus, many=True)
        return Response(serializer.data)


class MenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
