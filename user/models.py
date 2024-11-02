from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    USER_ROLES = [
        ('Admin', 'Admin'),
        ('Customer', 'Customer'),
        ('Driver', 'Driver'),
        ('Operator', 'Operator'),
    ]
    role = models.CharField(max_length=20, choices=USER_ROLES, default='Customer')

    def __str__(self):
        return f"{self.username} - {self.role}"


class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=50, unique=True)
    license_expiry_date = models.DateField()
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_number = models.CharField(max_length=15)
    vehicle_assigned = models.ForeignKey('website.Vehicle', on_delete=models.SET_NULL, null=True, blank=True)
    experience_years = models.IntegerField()

    def __str__(self):
        return f"Driver: {self.user.username}"


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    company_name = models.CharField(max_length=100, null=True, blank=True)
    gst_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return f"Customer: {self.user.username}"


class OperatorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='operator_profile')
    assigned_region = models.CharField(max_length=100)

    def __str__(self):
        return f"Operator: {self.user.username}"


class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {'Read' if self.read else 'Unread'}"
