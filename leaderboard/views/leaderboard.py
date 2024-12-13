from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from ..serializers.scoreofgame import LeaderboardSerializer, ScoreSerializer
from ..models import ScoreOfGame
from ..utility.pagination import Pagination
from rest_framework.permissions import AllowAny, IsAuthenticated


class GameLeaderboardView(APIView, Pagination):
    permission_classes = [AllowAny]
    serializer_class = LeaderboardSerializer

    @extend_schema(
        tags=['Leaderboards'],
        auth=[],
        summary= 'Leaderboard of a single game'
    )
    def get(self, request, game_name):
        game_scores = ScoreOfGame.objects.filter(game__name__contains=game_name).order_by('-score')
        for index, score in enumerate(game_scores, start=1):
            score.rank = index
        result = self.paginate_queryset(game_scores, request)
        serializer = LeaderboardSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class UserScoreView(APIView, Pagination):
    permission_classes = [IsAuthenticated]
    serializer_class = ScoreSerializer

    @extend_schema(
        tags=['Leaderboards'],
        summary='All user scores'
    )
    def get(self, request):
        scores = ScoreOfGame.objects.filter(user=request.user).order_by('-score')
        result = self.paginate_queryset(scores, request)
        serializer = ScoreSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class UserGameScoreView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScoreSerializer

    @extend_schema(
        tags=['Leaderboards'],
        summary='User score in a single game'
    )
    def get(self, request, game_name):
        try:
            score = ScoreOfGame.objects.get(user=request.user, game__name=game_name)
            serializer = ScoreSerializer(score)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ScoreOfGame.DoesNotExist:
            return Response({'error': 'Game Not Found'}, status=status.HTTP_404_NOT_FOUND)


class UserScoreSubmitView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LeaderboardSerializer

    @extend_schema(tags=['Submit Score'], methods=['POST'])
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            game = serializer.validated_data['game']
            score = serializer.validated_data['score']
            user = request.user

            # check if user has an existing score
            existing_score = ScoreOfGame.objects.filter(user=user, game=game).first()
            if existing_score:
                existing_score.score = score
                existing_score.save()
                return Response(
                    {"message": "Score updated successfully", "score": score},
                    status=status.HTTP_200_OK,
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=['Submit Score'], methods=['PUT'])
    def put(self, request):
        game_name = request.data.get('game')
        if not game_name:
            return Response({'error': 'Game is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:

            score_instance = ScoreOfGame.objects.get(user=request.user, game__name=game_name)
        except ScoreOfGame.DoesNotExist:
            return Response({'error': 'Score does not exist for this game.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(score_instance, data=request.data, partial=True,
                                           context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
