from django.urls import path
from .views import leaderboard

app_name = 'leaderboard'

urlpatterns = [
    path('game/<str:game_name>', leaderboard.GameLeaderboardView.as_view(), name='game-leaderboard'),
    path('user/<str:username>', leaderboard.UserScoreView.as_view(), name='user-scores'),
    path('<str:username>/<str:game_name>', leaderboard.UserGameScoreView.as_view(), name='user-game-score'),
    path('user/submit/', leaderboard.UserScoreSubmitView.as_view(), name='user-score-submit')
]
