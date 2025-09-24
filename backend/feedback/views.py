from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import Feedback
from .serializers import FeedbackSerializer


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
        return obj.created_by == request.user


class FeedbackCreateView(generics.CreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)


class UserFeedbackListView(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(created_by=self.request.user).select_related("created_by", "updated_by")


class AdminFeedbackListView(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    queryset = Feedback.objects.select_related("created_by", "updated_by").all()


class FeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    queryset = Feedback.objects.select_related("created_by", "updated_by")

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
