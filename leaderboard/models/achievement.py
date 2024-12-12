from django.db import models
from ..models import Game
from account.models import User


class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='achievements')
    min_score = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} earned {self.achievement.name}"
