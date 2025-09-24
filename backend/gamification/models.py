from django.conf import settings
from django.db import models


class UserGameInfo(models.Model):
    """Aggregated progress and energy information for a user."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="game_info",
    )
    xp_value = models.PositiveIntegerField(default=0)
    energy_value = models.PositiveIntegerField(default=0)
    energy_last_updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Game Info"
        verbose_name_plural = "User Game Infos"

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.user.username} game info"


class DailyStreak(models.Model):
    """Tracks each day that counts toward a user's streak."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_streaks",
    )
    daily_streak_date = models.DateField()

    class Meta:
        verbose_name = "Daily Streak"
        verbose_name_plural = "Daily Streaks"
        unique_together = ("user", "daily_streak_date")
        ordering = ["-daily_streak_date"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.user.username} streak on {self.daily_streak_date}"


class Achievement(models.Model):
    """Configurable targets that award a reward when met."""

    REWARD_XP = "xp"
    REWARD_ENERGY = "energy"
    REWARD_BADGE = "badge"

    REWARD_CHOICES = [
        (REWARD_XP, "XP"),
        (REWARD_ENERGY, "Energy"),
        (REWARD_BADGE, "Badge"),
    ]

    target_xp_value = models.PositiveIntegerField(null=True, blank=True)
    target_streak_value = models.PositiveIntegerField(null=True, blank=True)
    target_completed_test = models.ForeignKey(
        "courses.Test",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="achievement_targets",
    )
    reward_type = models.CharField(max_length=10, choices=REWARD_CHOICES)
    reward_amount = models.PositiveIntegerField(null=True, blank=True)
    reward_content = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"Achievement {self.pk}"


class UserClaimedAchievement(models.Model):
    """Join table linking a user to the achievements they have claimed."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="claimed_achievements",
    )
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name="claims",
    )
    claimed_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Claimed Achievement"
        verbose_name_plural = "User Claimed Achievements"
        unique_together = ("user", "achievement")
        ordering = ["-claimed_date"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.user.username} claimed {self.achievement_id}"
