from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    designer = models.CharField(max_length=255)
    year_released = models.DateField()
    number_of_players = models.IntegerField()
    estimated_time_to_play = models.CharField(max_length=255)
    age_recommendation = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")
    image_url = models.CharField(max_length=255)
    categories = models.ManyToManyField(
        "Category", through="GameCategory", related_name="games"
    )
