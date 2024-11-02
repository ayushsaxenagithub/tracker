from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from .models import Vehicle, Document, Expense, Trip, Customer


class VehicleListView(View):
    def get(self, request):
        vehicles = Vehicle.objects.all()
        return render(request, 'vehicle/vehicle_list.html', {'vehicles': vehicles})


class VehicleDetailView(View):
    def get(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        documents = Document.objects.filter(vehicle=vehicle)
        expenses = Expense.objects.filter(vehicle=vehicle)
        trips = Trip.objects.filter(vehicle=vehicle)
        return render(request, 'vehicle/vehicle_detail.html', {
            'vehicle': vehicle,
            'documents': documents,
            'expenses': expenses,
            'trips': trips,
        })


class VehicleCreateView(View):
    def get(self, request):
        return render(request, 'vehicle/vehicle_form.html')

    def post(self, request):
        if request.method == 'POST':
            chassiss_no = request.POST.get('chassiss_no')
            engine_no = request.POST.get('engine_no')
            registration_no = request.POST.get('registration_no')
            region = request.POST.get('region')
            state = request.POST.get('state')
            make = request.POST.get('make')
            model = request.POST.get('model')
            variant = request.POST.get('variant')
            transmission_type = request.POST.get('transmission_type')
            fuel_type = request.POST.get('fuel_type')
            seating_capacity = request.POST.get('seating_capacity')
            color = request.POST.get('color')
            asset_number_sequence = request.POST.get('asset_number_sequence')
            date_of_manufacture = request.POST.get('date_of_manufacture')
            insurance_valid_upto = request.POST.get('insurance_valid_upto')
            puc_valid_upto = request.POST.get('puc_valid_upto')
            fitness_valid_upto = request.POST.get('fitness_valid_upto')
            last_battery_change_date = request.POST.get('last_battery_change_date')
            last_service_date = request.POST.get('last_service_date')
            last_service_kms = request.POST.get('last_service_kms')
            next_service_due_kms = request.POST.get('next_service_due_kms')
            next_service_due_date = request.POST.get('next_service_due_date')
            gps_tracking_enabled = request.POST.get('gps_tracking_enabled') == 'on'
            owner_name = request.POST.get('owner_name')
            owner_contact = request.POST.get('owner_contact')
            purchase_date = request.POST.get('purchase_date')
            warranty_expiry_date = request.POST.get('warranty_expiry_date')

            vehicle = Vehicle(
                chassiss_no=chassiss_no,
                engine_no=engine_no,
                registration_no=registration_no,
                region=region,
                state=state,
                make=make,
                model=model,
                variant=variant,
                transmission_type=transmission_type,
                fuel_type=fuel_type,
                seating_capacity=seating_capacity,
                color=color,
                asset_number_sequence=asset_number_sequence,
                date_of_manufacture=date_of_manufacture,
                insurance_valid_upto=insurance_valid_upto,
                puc_valid_upto=puc_valid_upto,
                fitness_valid_upto=fitness_valid_upto,
                last_battery_change_date=last_battery_change_date,
                last_service_date=last_service_date,
                last_service_kms=last_service_kms,
                next_service_due_kms=next_service_due_kms,
                next_service_due_date=next_service_due_date,
                gps_tracking_enabled=gps_tracking_enabled,
                owner_name=owner_name,
                owner_contact=owner_contact,
                purchase_date=purchase_date,
                warranty_expiry_date=warranty_expiry_date
            )
            vehicle.save()
            return HttpResponseRedirect(reverse('vehicle_list'))
        return render(request, 'vehicle/vehicle_form.html')


class DocumentCreateView(View):
    def get(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        return render(request, 'document/document_form.html', {'vehicle': vehicle})

    def post(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        document_type = request.POST.get('document_type')
        document_file = request.FILES.get('document_file')
        expiry_date = request.POST.get('expiry_date')

        document = Document(
            vehicle=vehicle,
            document_type=document_type,
            document_file=document_file,
            expiry_date=expiry_date
        )
        document.save()
        return HttpResponseRedirect(reverse('vehicle_detail', args=[vehicle.id]))


class ExpenseCreateView(View):
    def get(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        return render(request, 'expense/expense_form.html', {'vehicle': vehicle})

    def post(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        expense_type = request.POST.get('expense_type')
        expense_date = request.POST.get('expense_date')
        amount = request.POST.get('amount')
        attachment = request.FILES.get('attachment')
        remarks = request.POST.get('remarks')
        service_center_name = request.POST.get('service_center_name')
        service_center_contact = request.POST.get('service_center_contact')

        expense = Expense(
            vehicle=vehicle,
            expense_type=expense_type,
            expense_date=expense_date,
            amount=amount,
            attachment=attachment,
            remarks=remarks,
            service_center_name=service_center_name,
            service_center_contact=service_center_contact
        )
        expense.save()
        return HttpResponseRedirect(reverse('vehicle_detail', args=[vehicle.id]))


class TripCreateView(View):
    def get(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        return render(request, 'trip/trip_form.html', {'vehicle': vehicle})

    def post(self, request, vehicle_id):
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        start_date = request.POST.get('start_date')
        start_time = request.POST.get('start_time')
        end_date = request.POST.get('end_date')
        end_time = request.POST.get('end_time')
        type_of_trip = request.POST.get('type_of_trip')
        start_location = request.POST.get('start_location')
        end_location = request.POST.get('end_location')
        destinations = request.POST.get('destinations')
        number_of_days = request.POST.get('number_of_days')
        driver_name = request.POST.get('driver_name')
        driver_number = request.POST.get('driver_number')
        driver_license_number = request.POST.get('driver_license_number')
        driver_address = request.POST.get('driver_address')
        fuel_cost_per_litre = request.POST.get('fuel_cost_per_litre')
        average_km_per_litre = request.POST.get('average_km_per_litre')
        start_km = request.POST.get('start_km')
        end_km = request.POST.get('end_km')
        total_fuel_cost = request.POST.get('total_fuel_cost')
        maintenance_per_km = request.POST.get('maintenance_per_km')
        total_maintenance_cost = request.POST.get('total_maintenance_cost')
        driver_wage = request.POST.get('driver_wage')
        state_tax = request.POST.get('state_tax')
        other_charges = request.POST.get('other_charges')
        carrier_cost = request.POST.get('carrier_cost')
        fastag_start_balance = request.POST.get('fastag_start_balance')
        fastag_end_balance = request.POST.get('fastag_end_balance')
        total_toll = request.POST.get('total_toll')
        per_km_charges = request.POST.get('per_km_charges')
        per_day_avg_km = request.POST.get('per_day_avg_km')
        minimum_kms_billing_per_day = request.POST.get('minimum_kms_billing_per_day')
        trip_status = request.POST.get('trip_status')
        remarks = request.POST.get('remarks')

        trip = Trip(
            vehicle=vehicle,
            start_date=start_date,
            start_time=start_time,
            end_date=end_date,
            end_time=end_time,
            type_of_trip=type_of_trip,
            start_location=start_location,
            end_location=end_location,
            destinations=destinations,
            number_of_days=number_of_days,
            driver_name=driver_name,
            driver_number=driver_number,
            driver_license_number=driver_license_number,
            driver_address=driver_address,
            fuel_cost_per_litre=fuel_cost_per_litre,
            average_km_per_litre=average_km_per_litre,
            start_km=start_km,
            end_km=end_km,
            total_fuel_cost=total_fuel_cost,
            maintenance_per_km=maintenance_per_km,
            total_maintenance_cost=total_maintenance_cost,
            driver_wage=driver_wage,
            state_tax=state_tax,
            other_charges=other_charges,
            carrier_cost=carrier_cost,
            fastag_start_balance=fastag_start_balance,
            fastag_end_balance=fastag_end_balance,
            total_toll=total_toll,
            per_km_charges=per_km_charges,
            per_day_avg_km=per_day_avg_km,
            minimum_kms_billing_per_day=minimum_kms_billing_per_day,
            trip_status=trip_status,
            remarks=remarks
        )
        trip.save()
        return HttpResponseRedirect(reverse('vehicle_detail', args=[vehicle.id]))


class CustomerListView(View):
    def get(self, request):
        customers = Customer.objects.all()
        return render(request, 'customer/customer_list.html', {'customers': customers})


class CustomerDetailView(View):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        return render(request, 'customer/customer_detail.html', {'customer': customer})


class CustomerCreateView(View):
    def get(self, request):
        return render(request, 'customer/customer_form.html')

    def post(self, request):
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        state = request.POST.get('state')
        city = request.POST.get('city')
        email = request.POST.get('email')
        address = request.POST.get('address')
        gst_number = request.POST.get('gst_number')

        customer = Customer(
            name=name,
            phone_number=phone_number,
            state=state,
            city=city,
            email=email,
            address=address,
            gst_number=gst_number
        )
        customer.save()
        return HttpResponseRedirect(reverse('customer_list'))
