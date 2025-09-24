from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Custom user model with application specific fields."""

    ROLE_STUDENT = "student"
    ROLE_LECTURER = "lecturer"
    ROLE_ADMIN = "admin"

    ROLE_CHOICES = [
        (ROLE_STUDENT, "Student"),
        (ROLE_LECTURER, "Lecturer"),
        (ROLE_ADMIN, "Admin"),
    ]

    email = models.EmailField(unique=True)
    profile_icon = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STUDENT)
    registration_date = models.DateTimeField(default=timezone.now)
    enable_email_notification = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.username

