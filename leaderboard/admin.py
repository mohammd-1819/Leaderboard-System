from django.contrib import admin
from .models import Game, ScoreOfGame, Achievement, UserAchievement

admin.site.register(Game)
admin.site.register(ScoreOfGame)
admin.site.register(Achievement)
admin.site.register(UserAchievement)
