from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "created_by", "created_date", "updated_by", "updated_date", "short_message")
    search_fields = ("created_by__username", "message")
    ordering = ("-created_date",)

    @staticmethod
    def short_message(obj):
        if len(obj.message) > 60:
            return f"{obj.message[:57]}..."
        return obj.message
