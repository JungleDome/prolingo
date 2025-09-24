from django.contrib import admin
from .models import Achievement, DailyStreak, UserClaimedAchievement, UserGameInfo


@admin.register(UserGameInfo)
class UserGameInfoAdmin(admin.ModelAdmin):
    list_display = ("user", "xp_value", "energy_value", "energy_last_updated_date")
    search_fields = ("user__username",)


@admin.register(DailyStreak)
class DailyStreakAdmin(admin.ModelAdmin):
    list_display = ("user", "daily_streak_date")
    list_filter = ("daily_streak_date",)
    search_fields = ("user__username",)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "target_xp_value",
        "target_streak_value",
        "target_completed_test",
        "reward_type",
        "reward_amount",
    )
    list_filter = ("reward_type",)
    search_fields = ("reward_content",)


@admin.register(UserClaimedAchievement)
class UserClaimedAchievementAdmin(admin.ModelAdmin):
    list_display = ("user", "achievement", "claimed_date")
    search_fields = ("user__username",)
    autocomplete_fields = ("achievement", "user")
