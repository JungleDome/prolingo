from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import PremiumSubscription
from .serializers import PremiumSubscriptionSerializer


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (getattr(request.user, "role", None) == "admin" or request.user.is_staff)
        )


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if getattr(request.user, "role", None) == "admin" or request.user.is_staff:
            return True
        return obj.user == request.user


class PremiumSubscriptionCreateView(generics.CreateAPIView):
    serializer_class = PremiumSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PremiumSubscriptionListView(generics.ListAPIView):
    serializer_class = PremiumSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PremiumSubscription.objects.filter(user=self.request.user).select_related("user")


class PremiumSubscriptionAdminListView(generics.ListAPIView):
    serializer_class = PremiumSubscriptionSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    queryset = PremiumSubscription.objects.select_related("user").all()


class PremiumSubscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PremiumSubscriptionSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    queryset = PremiumSubscription.objects.select_related("user")

    def perform_update(self, serializer):
        type_changed = "type" in serializer.validated_data
        instance = serializer.save()
        if type_changed:
            instance.end_date = None
            instance.save()
