from django.urls import path
from .views import leaderboard, achievement, game

app_name = 'leaderboard'

urlpatterns = [
    path('game/<str:game_name>/', leaderboard.GameLeaderboardView.as_view(), name='game-leaderboard'),
    path('user/', leaderboard.UserScoreView.as_view(), name='user-scores'),
    path('<str:game_name>/', leaderboard.UserGameScoreView.as_view(), name='user-game-score'),
    path('user/submit/', leaderboard.UserScoreSubmitView.as_view(), name='user-score-submit'),

    path('achievement/game/<str:game_name>/', achievement.GameAchievementsView.as_view(), name='game-achievements'),
    path('achievement/user/', achievement.UserAchievementsView.as_view(), name='user-achievements'),
    path('achievement/check/', achievement.CheckAndAddAchievementsView.as_view(),
         name='check-achievements'),

    path('game/list/', game.GameListView.as_view(), name='game-list'),
    path('game/detail/<str:game_name>', game.GameDetailView.as_view(), name='game-detail'),
]
