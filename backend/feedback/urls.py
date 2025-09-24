from django.urls import path

from . import views

urlpatterns = [
    path("feedback/", views.FeedbackCreateView.as_view(), name="feedback-create"),
    path("feedback/mine/", views.UserFeedbackListView.as_view(), name="feedback-mine"),
    path("feedback/all/", views.AdminFeedbackListView.as_view(), name="feedback-all"),
    path("feedback/<int:pk>/", views.FeedbackDetailView.as_view(), name="feedback-detail"),
]
