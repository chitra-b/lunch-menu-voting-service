# Generated by Django 5.1.1 on 2024-09-13 08:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("votings", "0002_remove_vote_voted_at_vote_voted_on"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="vote",
            unique_together={("user", "voted_on", "rank")},
        ),
    ]
