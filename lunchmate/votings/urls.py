from django.urls import path, include
from rest_framework.routers import DefaultRouter

from votings.views import VoteViewSet

router = DefaultRouter()
router.register("votes", VoteViewSet, basename="votes")


urlpatterns = [
    path("", include(router.urls)),
]
