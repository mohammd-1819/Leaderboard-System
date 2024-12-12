from rest_framework import serializers
from ..models import Achievement, UserAchievement


class AchievementSerializer(serializers.ModelSerializer):
    game = serializers.StringRelatedField()

    class Meta:
        model = Achievement
        fields = ['name', 'game', 'min_score']
        read_only_fields = ['description']


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer()

    class Meta:
        model = UserAchievement
        fields = ['achievement', 'earned_at']
