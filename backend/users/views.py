from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, UserSettings
from .serializers import UserSerializer, UserSettingsSerializer
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from stats.models import Stats
from server.schema import extend_schema_with_tags

class IsAdminRole(BasePermission):
    def has_permission(self, request, _):
        return bool(
            request.user and request.user.is_authenticated and getattr(request.user, "role", None) == "admin"
        )

@extend_schema_with_tags("Users")
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@extend_schema_with_tags("Account")
class ManageAccountView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@extend_schema_with_tags("Admin Users")
class AdminListUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

@extend_schema_with_tags("Admin Users")
class AdminManageUserView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

@extend_schema_with_tags("Admin Users")
class AdminDeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

@extend_schema_with_tags("Account")
class AccountSettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure settings exists (created in serializer, but guard anyway)
        settings, _ = UserSettings.objects.get_or_create(user=self.request.user)
        return settings

@extend_schema_with_tags("Authentication")
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(username=request.data.get("username"))
        try:
            stats = user.stats
            print(stats, user, response, request, args, kwargs)
            stats.reset_energy()
            stats.check_streak()
        except Stats.DoesNotExist:
            Stats.objects.create(user=user)
        return response
