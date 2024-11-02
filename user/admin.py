
# admin.py
from django.contrib import admin
from .models import User, DriverProfile, CustomerProfile, OperatorProfile, UserActivityLog, Notification


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_verified', 'is_active')
    list_filter = ('role', 'is_verified', 'is_active')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)


class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'license_expiry_date', 'vehicle_assigned')
    search_fields = ('user__username', 'license_number')


class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'gst_number')
    search_fields = ('user__username', 'company_name')


class OperatorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'assigned_region')
    search_fields = ('user__username', 'assigned_region')


class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    search_fields = ('user__username', 'action')
    list_filter = ('timestamp',)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'read')
    search_fields = ('user__username', 'message')
    list_filter = ('read', 'created_at')


admin.site.register(User, UserAdmin)
admin.site.register(DriverProfile, DriverProfileAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(OperatorProfile, OperatorProfileAdmin)
admin.site.register(UserActivityLog, UserActivityLogAdmin)
admin.site.register(Notification, NotificationAdmin)