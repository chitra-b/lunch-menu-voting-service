from django.db import models
from datetime import date
from restaurants.models import Menu
from django.utils.translation import gettext as _

from users.models import User


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    # For the new API version (points for ranked votes: 1st -> 3 points, 2nd -> 2 points, 3rd -> 1 point)
    rank = models.PositiveSmallIntegerField(
        choices=[(1, "1st"), (2, "2nd"), (3, "3rd")], default=1
    )
    points = models.IntegerField(default=3)

    voted_on = models.DateField(_("Date"), default=date.today)

    class Meta:
        # Ensure each user can only vote once per menu or have one rank per menu
        unique_together = ("user", "menu", "rank")
        unique_together = ("user", "voted_on", "rank")

    def __str__(self):
        return f"{self.user.username} voted {self.rank} for {self.menu}"
