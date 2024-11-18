from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from .models import DriverProfile, CustomerProfile, OperatorProfile, UserActivityLog, Notification
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'user/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'user/register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'user/register.html')

        # Create the user with basic fields
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        # Create role-specific profile
        if role == 'Driver':
            license_number = request.POST.get('license_number')
            license_expiry_date = request.POST.get('license_expiry_date')
            emergency_contact_name = request.POST.get('emergency_contact_name')
            emergency_contact_number = request.POST.get('emergency_contact_number')
            experience_years = request.POST.get('experience_years')
            DriverProfile.objects.create(
                user=user,
                license_number=license_number,
                license_expiry_date=license_expiry_date,
                emergency_contact_name=emergency_contact_name,
                emergency_contact_number=emergency_contact_number,
                experience_years=experience_years
            )
        elif role == 'Customer':
            company_name = request.POST.get('company_name')
            gst_number = request.POST.get('gst_number')
            CustomerProfile.objects.create(
                user=user,
                company_name=company_name,
                gst_number=gst_number
            )
        elif role == 'Operator':
            assigned_region = request.POST.get('assigned_region')
            OperatorProfile.objects.create(
                user=user,
                assigned_region=assigned_region
            )

        # Log the user in and redirect to dashboard
        login(request, user)
        return redirect('user_dashboard')
    else:
        return render(request, 'user/register.html')


@login_required
def user_dashboard(request):
    user = request.user
    if hasattr(user, 'driver_profile'):
        profile = get_object_or_404(DriverProfile, user=user)
        return render(request, 'user/driver_dashboard.html', {'profile': profile})
    elif hasattr(user, 'customer_profile'):
        profile = get_object_or_404(CustomerProfile, user=user)
        return render(request, 'user/customer_dashboard.html', {'profile': profile})
    elif hasattr(user, 'operator_profile'):
        profile = get_object_or_404(OperatorProfile, user=user)
        return render(request, 'user/operator_dashboard.html')
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
        user.save()

        # Update role-specific profile fields
        if hasattr(user, 'driver_profile'):
            profile = user.driver_profile
            profile.license_number = request.POST.get('license_number', profile.license_number)
            profile.license_expiry_date = request.POST.get('license_expiry_date', profile.license_expiry_date)
            profile.emergency_contact_name = request.POST.get('emergency_contact_name', profile.emergency_contact_name)
            profile.emergency_contact_number = request.POST.get('emergency_contact_number', profile.emergency_contact_number)
            profile.save()
        elif hasattr(user, 'customer_profile'):
            profile = user.customer_profile
            profile.company_name = request.POST.get('company_name', profile.company_name)
            profile.gst_number = request.POST.get('gst_number', profile.gst_number)
            profile.save()
        elif hasattr(user, 'operator_profile'):
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
        if not request.user.is_superuser and not hasattr(request.user, 'operator_profile'):
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        driver = get_object_or_404(DriverProfile, id=driver_id)
        vehicle_id = request.POST.get('vehicle_id')
        driver.vehicle_assigned_id = vehicle_id
        driver.save()
        return JsonResponse({'status': 'success'})
