# models.py

from django.db import models
from django.contrib.auth.models import User

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile', null=True, blank=True)
    license_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    license_expiry_date = models.DateField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=15, null=True, blank=True)
    vehicle_assigned = models.ForeignKey('website.Vehicle', on_delete=models.SET_NULL, null=True, blank=True)
    experience_years = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if self.user:
            return f"Driver: {self.user.username}"
        return "Unassigned Driver"


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile', null=True, blank=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    gst_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        if self.user:
            return f"Customer: {self.user.username}"
        return "Unassigned Customer"


class OperatorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='operator_profile')
    assigned_region = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.user:
            return f"Operator: {self.user.username}"
        return "Unassigned Operator"


class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.action} at {self.timestamp}"
        return f"Unknown User - {self.action} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        if self.user:
            return f"Notification for {self.user.username} - {'Read' if self.read else 'Unread'}"
        return "Notification for Unknown User"

    class Meta:
        ordering = ['-created_at']
