from rest_framework import serializers
from ..models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('name', 'description', 'release_date', 'is_active')



