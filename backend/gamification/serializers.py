from rest_framework import serializers

from .models import Achievement, DailyStreak, UserClaimedAchievement, UserGameInfo


class UserGameInfoSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = UserGameInfo
        fields = [
            "id",
            "user",
            "username",
            "xp_value",
            "energy_value",
            "energy_last_updated_date",
        ]
        read_only_fields = ["id", "user", "username", "energy_last_updated_date"]


class DailyStreakSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = DailyStreak
        fields = ["id", "user", "username", "daily_streak_date"]
        read_only_fields = ["id", "user", "username"]


class AchievementSerializer(serializers.ModelSerializer):
    target_completed_test_title = serializers.ReadOnlyField(source="target_completed_test.chapter.title")

    class Meta:
        model = Achievement
        fields = [
            "id",
            "target_xp_value",
            "target_streak_value",
            "target_completed_test",
            "target_completed_test_title",
            "reward_type",
            "reward_amount",
            "reward_content",
        ]


class UserClaimedAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)
    achievement_id = serializers.PrimaryKeyRelatedField(
        queryset=Achievement.objects.all(), source="achievement", write_only=True
    )
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = UserClaimedAchievement
        fields = [
            "id",
            "user",
            "username",
            "achievement",
            "achievement_id",
            "claimed_date",
        ]
        read_only_fields = ["id", "user", "username", "achievement", "claimed_date"]
