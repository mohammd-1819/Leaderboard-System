from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from ..serializers import GameSerializer
from ..models import Game
from ..utility.pagination import Pagination
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404


class GameListView(APIView, Pagination):
    permission_classes = [AllowAny]
    serializer_class = GameSerializer

    @extend_schema(
        tags=['Game'],
        summary='List of Games',
        auth=[]
    )
    def get(self, request):
        games = Game.objects.all()
        result = self.paginate_queryset(games, request)
        serializer = GameSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class GameDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = GameSerializer

    @extend_schema(
        tags=['Game'],
        summary='Details of a single Game',
        auth=[]
    )
    def get(self, request, game_name):
        try:
            game = get_object_or_404(Game, name=game_name)
            serializer = GameSerializer(instance=game)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Game Not Found'}, status=status.HTTP_404_NOT_FOUND)
