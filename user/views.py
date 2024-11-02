from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from .models import User, DriverProfile, CustomerProfile, OperatorProfile, UserActivityLog, Notification


@login_required
def user_dashboard(request):
    user = request.user
    if user.role == 'Driver':
        profile = get_object_or_404(DriverProfile, user=user)
        return render(request, 'user/driver_dashboard.html', {'profile': profile})
    elif user.role == 'Customer':
        profile = get_object_or_404(CustomerProfile, user=user)
        return render(request, 'user/customer_dashboard.html', {'profile': profile})
    elif user.role == 'Operator':
        profile = get_object_or_404(OperatorProfile, user=user)
        return render(request, 'user/operator_dashboard.html', {'profile': profile})
    else:
        return render(request, 'user/admin_dashboard.html')


@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        # Update user fields
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.address = request.POST.get('address', user.address)
        user.save()

        # Update role-specific profile fields
        if user.role == 'Driver':
            profile = user.driver_profile
            profile.license_number = request.POST.get('license_number', profile.license_number)
            profile.license_expiry_date = request.POST.get('license_expiry_date', profile.license_expiry_date)
            profile.emergency_contact_name = request.POST.get('emergency_contact_name', profile.emergency_contact_name)
            profile.emergency_contact_number = request.POST.get('emergency_contact_number', profile.emergency_contact_number)
            profile.save()
        elif user.role == 'Customer':
            profile = user.customer_profile
            profile.company_name = request.POST.get('company_name', profile.company_name)
            profile.gst_number = request.POST.get('gst_number', profile.gst_number)
            profile.save()
        elif user.role == 'Operator':
            profile = user.operator_profile
            profile.assigned_region = request.POST.get('assigned_region', profile.assigned_region)
            profile.save()

        return HttpResponseRedirect(reverse('user_dashboard'))

    return render(request, 'user/update_profile.html', {'user': user})


class NotificationView(View):
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user, read=False)
        return render(request, 'user/notifications.html', {'notifications': notifications})

    def post(self, request):
        notification_id = request.POST.get('notification_id')
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.read = True
        notification.save()
        return JsonResponse({'status': 'success'})


@login_required
def user_activity_log(request):
    logs = UserActivityLog.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'user/activity_log.html', {'logs': logs})


class UserListView(View):
    def get(self, request):
        if not request.user.is_superuser:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        users = User.objects.all()
        return render(request, 'user/user_list.html', {'users': users})


class AssignVehicleToDriverView(View):
    def post(self, request, driver_id):
        if not request.user.is_superuser and request.user.role != 'Operator':
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        driver = get_object_or_404(DriverProfile, id=driver_id)
        vehicle_id = request.POST.get('vehicle_id')
        driver.vehicle_assigned_id = vehicle_id
        driver.save()
        return JsonResponse({'status': 'success'})
