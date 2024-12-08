from django.db import models
from account.models import User
from ..models import Game


class ScoreOfGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='scores')
    score = models.PositiveIntegerField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score']
        indexes = [
            models.Index(fields=['game', '-score']),
        ]

    def __str__(self):
        return f"{self.user.username}' score"
