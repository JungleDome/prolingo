from django.conf import settings
from django.db import models


class Feedback(models.Model):
    message = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="feedback_created",
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="feedback_updated",
    )
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"Feedback {self.pk}"
