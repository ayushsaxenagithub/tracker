from django.db import models

class Vehicle(models.Model):
    chassiss_no = models.CharField(max_length=50, unique=True)
    engine_no = models.CharField(max_length=50, unique=True)
    registration_no = models.CharField(max_length=20, unique=True)
    region = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    variant = models.CharField(max_length=50)
    transmission_type = models.CharField(max_length=20, choices=[('Manual', 'Manual'), ('Automatic', 'Automatic')])
    fuel_type = models.CharField(max_length=20, choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Electric', 'Electric'), ('Hybrid', 'Hybrid')])
    seating_capacity = models.IntegerField()
    color = models.CharField(max_length=30)
    asset_number_sequence = models.CharField(max_length=100)
    date_of_manufacture = models.DateField()
    insurance_valid_upto = models.DateField()
    puc_valid_upto = models.DateField()
    fitness_valid_upto = models.DateField()
    last_battery_change_date = models.DateField(null=True, blank=True)
    last_service_date = models.DateField(null=True, blank=True)
    last_service_kms = models.IntegerField(null=True, blank=True)
    next_service_due_kms = models.IntegerField(null=True, blank=True)
    next_service_due_date = models.DateField(null=True, blank=True)
    gps_tracking_enabled = models.BooleanField(default=False)
    owner_name = models.CharField(max_length=100)
    owner_contact = models.CharField(max_length=15)
    purchase_date = models.DateField()
    warranty_expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.registration_no} - {self.make} {self.model}"


class Document(models.Model):
    VEHICLE_DOCUMENT_TYPES = [
        ('Insurance', 'Insurance'),
        ('RC', 'RC'),
        ('PUC', 'PUC'),
        ('Fitness Certificate', 'Fitness Certificate'),
        ('Warranty', 'Warranty'),
        ('Permit', 'Permit'),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=VEHICLE_DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='documents/')
    upload_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle.registration_no} - {self.document_type}"


class Expense(models.Model):
    EXPENSE_TYPES = [
        ('Paid Service', 'Paid Service'),
        ('General Repair', 'General Repair'),
        ('Damage Repair', 'Damage Repair'),
        ('Insurance Renewal', 'Insurance Renewal'),
        ('PUC Renewal', 'PUC Renewal'),
        ('Fitness Renewal', 'Fitness Renewal'),
        ('Fuel', 'Fuel'),
        ('Tyre', 'Tyre'),
        ('Battery', 'Battery'),
        ('Washing', 'Washing'),
        ('Detailing', 'Detailing'),
        ('Toll', 'Toll'),
        ('Parking', 'Parking'),
        ('Others', 'Others'),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=50, choices=EXPENSE_TYPES)
    expense_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    attachment = models.FileField(upload_to='expenses/', null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    service_center_name = models.CharField(max_length=100, null=True, blank=True)
    service_center_contact = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle.registration_no} - {self.expense_type} on {self.expense_date}"


class Trip(models.Model):
    TRIP_TYPES = [
        ('Local', 'Local'),
        ('Outstation Per KM', 'Outstation Per KM'),
        ('Outstation Lump Sum', 'Outstation Lump Sum'),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    type_of_trip = models.CharField(max_length=50, choices=TRIP_TYPES)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    destinations = models.TextField()
    number_of_days = models.IntegerField()
    driver_name = models.CharField(max_length=100)
    driver_number = models.CharField(max_length=15)
    driver_license_number = models.CharField(max_length=50)
    driver_address = models.CharField(max_length=200)
    fuel_cost_per_litre = models.DecimalField(max_digits=6, decimal_places=2)
    average_km_per_litre = models.DecimalField(max_digits=6, decimal_places=2)
    start_km = models.IntegerField()
    end_km = models.IntegerField()
    total_fuel_cost = models.DecimalField(max_digits=10, decimal_places=2)
    maintenance_per_km = models.DecimalField(max_digits=6, decimal_places=2)
    total_maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2)
    driver_wage = models.DecimalField(max_digits=10, decimal_places=2)
    state_tax = models.DecimalField(max_digits=10, decimal_places=2)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2)
    carrier_cost = models.DecimalField(max_digits=10, decimal_places=2)
    fastag_start_balance = models.DecimalField(max_digits=10, decimal_places=2)
    fastag_end_balance = models.DecimalField(max_digits=10, decimal_places=2)
    total_toll = models.DecimalField(max_digits=10, decimal_places=2)
    per_km_charges = models.DecimalField(max_digits=6, decimal_places=2)
    per_day_avg_km = models.DecimalField(max_digits=6, decimal_places=2)
    minimum_kms_billing_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    trip_status = models.CharField(max_length=50, choices=[('Planned', 'Planned'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed')])
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Trip for {self.vehicle.registration_no} from {self.start_date} to {self.end_date}"


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    address = models.TextField()
    gst_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name
