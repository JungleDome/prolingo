from django.urls import path

from . import views

urlpatterns = [
    path("game-info/", views.UserGameInfoView.as_view(), name="user-game-info"),
    path("game-info/all/", views.UserGameInfoListView.as_view(), name="admin-game-info-list"),
    path("daily-streaks/", views.DailyStreakListCreateView.as_view(), name="daily-streaks"),
    path("daily-streaks/all/", views.DailyStreakAdminListView.as_view(), name="admin-daily-streaks"),
    path("achievements/", views.AchievementListCreateView.as_view(), name="achievements"),
    path("achievements/<int:pk>/", views.AchievementDetailView.as_view(), name="achievement-detail"),
    path("claimed-achievements/", views.UserClaimedAchievementListView.as_view(), name="claimed-achievements"),
    path("claimed-achievements/claim/", views.ClaimAchievementView.as_view(), name="claim-achievement"),
    path(
        "claimed-achievements/all/",
        views.AdminClaimedAchievementListView.as_view(),
        name="admin-claimed-achievements",
    ),
]
