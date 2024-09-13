from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F
from django.utils import timezone

from votings.models import Vote
from votings.serializers import VoteSerializer
from users.permissions import IsEmployee


class VoteViewSet(ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsEmployee]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Check API version from request headers
        api_version = request.headers.get("API-Version")

        if api_version == "1.0":
            # Old version: user can vote for one menu
            if Vote.objects.filter(
                user=request.user, menu=request.data["menu"]
            ).exists():
                raise ValidationError("You have already voted for this menu.")
            request.data["rank"] = 1
            return super().create(request, *args, **kwargs)

        elif api_version == "2.0":
            # New version: user can vote for up to three menus
            current_date = timezone.now().date()
            existing_votes = Vote.objects.filter(
                user=request.user, voted_on=current_date
            )
            if (
                existing_votes.count() >= 3
                or len(request.data) > 3
                or existing_votes.count() + len(request.data) > 3
            ):
                raise ValidationError("You can only vote for up to three menus.")

            # for each_vote in request.data:
            serializer = self.get_serializer(data=request.data["votes"], many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data)

        return Response({"detail": "Unsupported API version."}, status=400)

    @action(detail=False, methods=["get"], url_path="current-day-results")
    def current_day_results(self, request):
        # Get the current date
        current_date = timezone.now().date()

        # Get votes for today's menus and aggregate total points for each menu
        results = (
            Vote.objects.filter(menu__date=current_date)
            .values("menu__id")
            .annotate(
                total_points=Sum("points"),
                menu_id=F("menu__id"),
                restaurant_name=F("menu__restaurant__name"),
                menu_date=F("menu__date"),
            )
            .values("total_points", "menu_id", "restaurant_name", "menu_date")
            .order_by("-total_points")
        )

        return Response({"date": current_date, "results": results})
