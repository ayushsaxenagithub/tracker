# urls.py
from django.urls import path, include
from . import views
from .views import NotificationView, UserListView, AssignVehicleToDriverView

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('notifications/', NotificationView.as_view(), name='notifications'),
    path('activity-log/', views.user_activity_log, name='user_activity_log'),
    path('user-list/', UserListView.as_view(), name='user_list'),
    path('assign-vehicle/<int:driver_id>/', AssignVehicleToDriverView.as_view(), name='assign_vehicle'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/',views.user_logout, name='logout'),
]


