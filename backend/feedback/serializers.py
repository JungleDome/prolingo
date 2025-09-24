from rest_framework import serializers

from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source="created_by.username")
    updated_by_username = serializers.ReadOnlyField(source="updated_by.username")

    class Meta:
        model = Feedback
        fields = [
            "id",
            "message",
            "created_by",
            "created_by_username",
            "created_date",
            "updated_by",
            "updated_by_username",
            "updated_date",
        ]
        read_only_fields = [
            "id",
            "created_by",
            "created_by_username",
            "created_date",
            "updated_by_username",
            "updated_date",
        ]
