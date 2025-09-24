from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import Achievement, DailyStreak, UserClaimedAchievement, UserGameInfo
from .serializers import (
    AchievementSerializer,
    DailyStreakSerializer,
    UserClaimedAchievementSerializer,
    UserGameInfoSerializer,
)


class IsAdminRole(BasePermission):
    """Shared admin-role permission used across the project."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (getattr(request.user, "role", None) == "admin" or request.user.is_staff)
        )


class UserGameInfoView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the current user's game info."""

    serializer_class = UserGameInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj, _ = UserGameInfo.objects.get_or_create(user=self.request.user)
        return obj


class UserGameInfoListView(generics.ListAPIView):
    """Allow admins to browse all user game information records."""

    serializer_class = UserGameInfoSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    queryset = UserGameInfo.objects.select_related("user").all()


class DailyStreakListCreateView(generics.ListCreateAPIView):
    """List the authenticated user's streak history or add a new entry."""

    serializer_class = DailyStreakSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailyStreak.objects.filter(user=self.request.user).order_by("-daily_streak_date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DailyStreakAdminListView(generics.ListAPIView):
    serializer_class = DailyStreakSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    queryset = DailyStreak.objects.select_related("user").all()


class AchievementListCreateView(generics.ListCreateAPIView):
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    queryset = Achievement.objects.all().select_related("target_completed_test", "target_completed_test__chapter")


class AchievementDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    queryset = Achievement.objects.all().select_related("target_completed_test", "target_completed_test__chapter")


class UserClaimedAchievementListView(generics.ListAPIView):
    serializer_class = UserClaimedAchievementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            UserClaimedAchievement.objects.select_related("achievement", "achievement__target_completed_test", "user")
            .filter(user=self.request.user)
            .order_by("-claimed_date")
        )


class ClaimAchievementView(generics.CreateAPIView):
    serializer_class = UserClaimedAchievementSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AdminClaimedAchievementListView(generics.ListAPIView):
    serializer_class = UserClaimedAchievementSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    queryset = UserClaimedAchievement.objects.select_related("achievement", "user").all()
