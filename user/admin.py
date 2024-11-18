# admin.py

from django.contrib import admin
from .models import DriverProfile, CustomerProfile, OperatorProfile, UserActivityLog, Notification

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'license_expiry_date', 'vehicle_assigned', 'experience_years')
    search_fields = ('user__username', 'license_number', 'emergency_contact_name')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'gst_number')
    search_fields = ('user__username', 'company_name', 'gst_number')


@admin.register(OperatorProfile)
class OperatorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'assigned_region')
    search_fields = ('user__username', 'assigned_region')


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    search_fields = ('user__username', 'action')
    list_filter = ('timestamp',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'read')
    search_fields = ('user__username', 'message')
    list_filter = ('read', 'created_at')
