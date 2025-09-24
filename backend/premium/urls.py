from django.urls import path

from . import views

urlpatterns = [
    path("subscriptions/", views.PremiumSubscriptionListView.as_view(), name="subscription-list"),
    path("subscriptions/create/", views.PremiumSubscriptionCreateView.as_view(), name="subscription-create"),
    path("subscriptions/all/", views.PremiumSubscriptionAdminListView.as_view(), name="subscription-all"),
    path("subscriptions/<int:pk>/", views.PremiumSubscriptionDetailView.as_view(), name="subscription-detail"),
]
