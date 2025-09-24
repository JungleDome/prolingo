from rest_framework import serializers

from .models import PremiumSubscription


class PremiumSubscriptionSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = PremiumSubscription
        fields = [
            "id",
            "user",
            "username",
            "type",
            "start_date",
            "end_date",
            "tier",
            "is_active",
        ]
        read_only_fields = ["id", "user", "username", "start_date", "end_date", "is_active"]

    def get_is_active(self, obj):
        return obj.is_active()
