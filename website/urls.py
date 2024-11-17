# urls.py
from django.urls import path
from .views import VehicleListView, VehicleDetailView, VehicleCreateView, DocumentCreateView, ExpenseCreateView, TripCreateView, CustomerListView, CustomerDetailView, CustomerCreateView

urlpatterns = [
    path('', VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/<int:vehicle_id>/', VehicleDetailView.as_view(), name='vehicle_detail'),
    path('vehicles/create/', VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicles/<int:vehicle_id>/documents/create/', DocumentCreateView.as_view(), name='document_create'),
    path('vehicles/<int:vehicle_id>/expenses/create/', ExpenseCreateView.as_view(), name='expense_create'),
    path('vehicles/<int:vehicle_id>/trips/create/', TripCreateView.as_view(), name='trip_create'),
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:customer_id>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/create/', CustomerCreateView.as_view(), name='customer_create'),
]

