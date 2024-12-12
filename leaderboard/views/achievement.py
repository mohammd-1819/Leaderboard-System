from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from ..models import Achievement, UserAchievement
from ..serializers import AchievementSerializer, UserAchievementSerializer
from ..models import Game, ScoreOfGame


class GameAchievementsView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AchievementSerializer

    @extend_schema(
        tags=['Achievements'],
        summary="Achievements of a Game",
        auth=[]
    )
    def get(self, request, game_name):
        achievements = Achievement.objects.filter(game__name=game_name)
        if not achievements.exists():
            return Response({"message": "No achievements found for this game."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AchievementSerializer(achievements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAchievementsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAchievementSerializer

    @extend_schema(
        tags=['Achievements'],
        summary="Achievements of a User",
    )
    def get(self, request):
        user_achievements = UserAchievement.objects.filter(user=request.user)
        if not user_achievements.exists():
            return Response({"message": "You have not earned any achievements yet."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserAchievementSerializer(user_achievements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckAndAddAchievementsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Achievements'],
        summary="Check and Add Achievements for a User",
        request=inline_serializer(
            name="AchievementCheckRequest",
            fields={
                "game_name": serializers.CharField(),
            },
        ),
        responses={
            200: inline_serializer(
                name="AchievementResponse",
                fields={
                    "message": serializers.CharField(),
                    "new_achievements": serializers.ListField(
                        child=serializers.CharField(), required=False
                    ),
                },
            )
        }
    )
    def post(self, request):
        game_name = request.data.get("game_name")

        # Validate game existence
        try:
            game = Game.objects.get(name=game_name)
        except Game.DoesNotExist:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        # Fetch user's highest score for the game
        user_score = ScoreOfGame.objects.filter(user=request.user, game=game).order_by('-score').first()
        if not user_score:
            return Response({"error": "No scores found for this game."}, status=status.HTTP_404_NOT_FOUND)

        highest_score = user_score.score

        # Fetch achievements based on the score
        achievements = Achievement.objects.filter(game=game, min_score__lte=highest_score)

        # Exclude already earned achievements
        new_achievements = achievements.exclude(
            id__in=UserAchievement.objects.filter(user=request.user).values_list('achievement_id', flat=True)
        )

        # Create new achievements
        UserAchievement.objects.bulk_create([
            UserAchievement(user=request.user, achievement=achievement) for achievement in new_achievements
        ])

        if not new_achievements:
            return Response({"message": "No new achievements earned."}, status=status.HTTP_200_OK)

        achievement_names = [achievement.name for achievement in new_achievements]
        return Response(
            {
                "message": "New achievements earned!",
                "new_achievements": achievement_names,
            },
            status=status.HTTP_201_CREATED
        )
