from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import EMPLOYEE, RESTAURANT_OWNER, ADMIN


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit/delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Return False for unauthenticated user
        if not bool(request.user and request.user.is_authenticated):
            return False
        # Allow admins to edit or delete any user
        if request.user.is_superuser:
            return True
        # Allow users to edit/delete their own profile
        return obj.id == request.user.id


class IsRestaurantOwner(BasePermission):
    """
    Custom permission to allow only restaurant owners to manage restaurant data.
    """

    def has_permission(self, request, view):
        # Return False for unauthenticated user
        if not bool(request.user and request.user.is_authenticated):
            return False
        # Allow access if the user is a restaurant owner
        return request.user.role == RESTAURANT_OWNER


class IsEmployee(BasePermission):
    """
    Custom permission to allow only employees.
    """

    def has_permission(self, request, view):
        # Return False for unauthenticated user
        if not bool(request.user and request.user.is_authenticated):
            return False
        # Allow access if the user is a restaurant owner
        return request.user.role == EMPLOYEE


class IsAdminUser(BasePermission):
    """
    Custom permission to restrict access to admins only.
    """

    def has_permission(self, request, view):
        # Return False for unauthenticated user
        if not bool(request.user and request.user.is_authenticated):
            return False
        return request.user.is_superuser or request.user.role == ADMIN


class IsRestaurantOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        # Return False for unauthenticated user for write apis
        if not bool(request.user and request.user.is_authenticated):
            return False
        # Write permissions are only allowed to the owner of the restaurant
        return obj.restaurant.owner == request.user
