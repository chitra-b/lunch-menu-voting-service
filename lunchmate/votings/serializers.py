from rest_framework import serializers
from votings.models import Vote
from restaurants.serializers import MenuSerializer


class VoteSerializer(serializers.ModelSerializer):
    # menu = MenuSerializer()

    class Meta:
        model = Vote
        fields = ["id", "user", "menu", "rank", "points", "voted_on"]
        read_only_fields = ["user", "voted_on"]

    def validate(self, data):
        # If the rank is provided, calculate points based on the rank
        if "rank" in data:
            rank = data["rank"]
            if rank == 1:
                data["points"] = 3
            elif rank == 2:
                data["points"] = 2
            elif rank == 3:
                data["points"] = 1
            else:
                raise serializers.ValidationError("Rank must be 1, 2, or 3.")
        return data
