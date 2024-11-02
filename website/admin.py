
# admin.py
from django.contrib import admin
from .models import Vehicle, Document, Expense, Trip, Customer


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('registration_no', 'make', 'model', 'owner_name', 'state')
    search_fields = ('registration_no', 'chassiss_no', 'engine_no', 'make', 'model')
    list_filter = ('state', 'make', 'fuel_type')


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'document_type', 'expiry_date')
    search_fields = ('vehicle__registration_no', 'document_type')
    list_filter = ('document_type', 'expiry_date')


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'expense_type', 'expense_date', 'amount')
    search_fields = ('vehicle__registration_no', 'expense_type')
    list_filter = ('expense_type', 'expense_date')


class TripAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'start_date', 'end_date', 'type_of_trip', 'driver_name')
    search_fields = ('vehicle__registration_no', 'driver_name', 'type_of_trip')
    list_filter = ('type_of_trip', 'start_date', 'end_date')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'city', 'email')
    search_fields = ('name', 'phone_number', 'email')
    list_filter = ('state', 'city')


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Customer, CustomerAdmin)