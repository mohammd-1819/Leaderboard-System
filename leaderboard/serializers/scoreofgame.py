from rest_framework import serializers
from ..models import ScoreOfGame, Game


class LeaderboardSerializer(serializers.ModelSerializer):
    game = serializers.SlugRelatedField(slug_field='name', queryset=Game.objects.all())
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)
    rank = serializers.IntegerField(read_only=True)

    class Meta:
        model = ScoreOfGame
        fields = ('user', 'game', 'score', 'rank')
        read_only_fields = ('user', 'rank', 'created_at',)

    def validate_game(self, value):
        if not value:
            raise serializers.ValidationError('invalid game')
        return value

    def validate_score(self, value: int):
        if value < 0:
            raise serializers.ValidationError('score cannot be a negative value')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        game = validated_data['game']
        score, created = ScoreOfGame.objects.update_or_create(
            user=user, game=game,
            defaults={'score': validated_data['score']}
        )
        return score

    def update(self, instance, validated_data):
        instance.score = validated_data.get('score', instance.score)
        instance.save()
        return instance


class ScoreSerializer(serializers.ModelSerializer):
    game = serializers.StringRelatedField()

    class Meta:
        model = ScoreOfGame
        fields = ('game', 'score')
        read_only_fields = ('created_at',)
