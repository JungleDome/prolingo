from django.contrib import admin

from .models import PremiumSubscription


@admin.register(PremiumSubscription)
class PremiumSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "tier", "start_date", "end_date")
    list_filter = ("type", "tier")
    search_fields = ("user__username",)
    ordering = ("-start_date",)
