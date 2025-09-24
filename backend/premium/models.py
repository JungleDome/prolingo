from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta


class PremiumSubscription(models.Model):
    TYPE_MONTH = "month"
    TYPE_YEAR = "year"
    TYPE_CHOICES = [
        (TYPE_MONTH, "Monthly"),
        (TYPE_YEAR, "Yearly"),
    ]

    TIER_ONE = 1
    TIER_TWO = 2
    TIER_THREE = 3
    TIER_CHOICES = [
        (TIER_ONE, "Tier 1"),
        (TIER_TWO, "Tier 2"),
        (TIER_THREE, "Tier 3"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="premium_subscriptions")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    tier = models.PositiveSmallIntegerField(choices=TIER_CHOICES, default=TIER_ONE)

    class Meta:
        ordering = ["-start_date"]

    def save(self, *args, **kwargs):
        if not self.end_date:
            duration = timedelta(days=365) if self.type == self.TYPE_YEAR else timedelta(days=30)
            self.end_date = self.start_date + duration
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.user} - {self.type}"

    def is_active(self) -> bool:
        now = timezone.now()
        return self.start_date <= now <= self.end_date
