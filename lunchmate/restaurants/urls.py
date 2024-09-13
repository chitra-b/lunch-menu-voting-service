from django.urls import path, include
from rest_framework.routers import DefaultRouter

from restaurants.views import RestaurantViewSet, MenuViewSet, MenuItemViewSet

router = DefaultRouter()
router.register("restaurants", RestaurantViewSet, basename="restaurants")
router.register("menus", MenuViewSet, basename="menus")
router.register("menu-items", MenuItemViewSet, basename="menu-items")

urlpatterns = [
    path("", include(router.urls)),
]
