from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.core import serializers
import json, copy
from promo_diskon.models import DiscEntry
from promo_diskon.forms import DiscEntryForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.utils.html import strip_tags
from .models import RumahMakan
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User

# Create your views here.
def show_main(request):
    disc_entries = DiscEntry.objects.all()
    restaurants = RumahMakan.objects.all()
    context = {
        'disc_entries': disc_entries,
        'restaurants': restaurants
    }
    return render(request, "promo_main.html", context)

@login_required
def create_disc_entry(request):
    form = DiscEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('promo_diskon:show_main')

    context = {'form': form}
    return render(request, "create_disc_entry.html", context)

@csrf_exempt
@require_POST
@login_required(login_url='/profil/login')
def add_disc_entry_ajax(request):
    form = DiscEntryForm(request.POST)

    if form.is_valid():
        disc = form.save(commit=False)  # Save the disc without committing yet
        
        # Fetch the restaurant by name from the rumahmakan model
        resto_name = request.POST.get('resto')
        try:
            restaurant = RumahMakan.objects.get(nama=resto_name)
            disc.resto = restaurant.nama  # Assign the found restaurant object (or UUID)
        except RumahMakan.DoesNotExist:
            return JsonResponse({"error": "Restaurant not found"}, status=400)

        disc.user = request.user  # Set the user manually
        disc.save()  # Now save the object
        return JsonResponse({"message": "Discount entry created successfully"}, status=201)
    else:
        # Send back an error message with status 400
        error_message = ', '.join([f"{field}: {error[0]}" for field, error in form.errors.items()])
        return JsonResponse({"error": f"Error: {error_message}"}, status=400)

@login_required(login_url='/profil/login')
def edit_disc_entry(request, id):
    # Get discount entry based on id
    discount = DiscEntry.objects.get(pk=id)
    resto = discount.resto
    resto_obj = RumahMakan.objects.get(nama=resto)
    resto_name = resto_obj.nama
    
    # Set discount entry as instance of form
    form = DiscEntryForm(request.POST or None, instance=discount)

    if form.is_valid() and request.method == "POST":
        # Save the form and redirect to the main page
        temp = form.save(commit=False)
        resto_name = request.POST.get('resto')
        try:
            restaurant = RumahMakan.objects.get(nama=resto_name)
            temp.resto = restaurant.nama  # Assign the found restaurant object (or UUID)
        except RumahMakan.DoesNotExist:
            return JsonResponse({"error": "Restaurant not found"}, status=400)
        
        temp.user=request.user
        temp.save()
        return HttpResponseRedirect(reverse('promo_diskon:show_main'))
    
    context = {
        'form': form,
        'resto_name': resto_name
    }
    return render(request, "edit_disc.html", context)
    
@login_required(login_url='/profil/login')
def delete_disc(request, id):
    # Get product berdasarkan id
    disc = DiscEntry.objects.get(pk = id)
    # Hapus product
    disc.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('promo_diskon:show_main'))

@csrf_exempt
def add_disc_entry_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            print(data)
            # Validate required fields first
            required_fields = ['code', 'resto', 'percentage', 'min_payment', 'valid_period']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({"error": f"Missing field: {field}"}, status=400)
            
            # Create new discount entry
            discount = DiscEntry()
            
            # Set user
            try:
                dummy_user = User.objects.get(id=5)
            except User.DoesNotExist:
                # Create user if doesn't exist
                dummy_user = User.objects.create_user(
                    id=5,
                    username='dummy_user',
                    email='dummy@example.com',
                    password='dummypassword'
                )
            
            discount.user = dummy_user
            
            # print("tes")
            
            # Set restaurant
            resto_name = data.get('resto')
            try:
                restaurant = RumahMakan.objects.get(nama=resto_name)
                discount.resto = restaurant.nama
            except RumahMakan.DoesNotExist:
                return JsonResponse({"error": "Restaurant not found"}, status=402)
            
            # Set other fields
            discount.code = data.get('code')
            try:
                discount.percentage = int(data.get('percentage'))
                discount.min_payment = int(data.get('min_payment'))
            except ValueError:
                return JsonResponse({"error": "Invalid number format for percentage or min_payment"}, status=403)
            
            # Set valid period
            try:
                discount.valid_period = datetime.strptime(data.get('valid_period'), '%Y-%m-%d').date()
            except (ValueError, TypeError):
                return JsonResponse({"error": "Invalid date format for valid_period. Use YYYY-MM-DD."}, status=405)
            
            # Save the discount entry
            discount.save()
            
            return JsonResponse({
                "status": "success",
                "message": "Successfully created discount entry!",
                "discount": {
                    "user": discount.user.id,
                    "code": discount.code,
                    "resto": discount.resto,
                    "percentage": discount.percentage,
                    "min_payment": discount.min_payment,
                    "valid_period": discount.valid_period.strftime('%Y-%m-%d')
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=407)
        except Exception as e:
            print(f"Exception: {str(e)}")  # Debug print
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=408)
    
@csrf_exempt
def edit_disc_entry_flutter(request, id):
    if request.method in ['PUT', 'PATCH', 'POST']:
        try:
            discount = DiscEntry.objects.get(pk=id)
        except DiscEntry.DoesNotExist:
            return JsonResponse({"error": "DiscEntry not found"}, status=404)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Validate required fields
        required_fields = ['code', 'resto', 'percentage', 'min_payment', 'valid_period']
        for field in required_fields:
            if field not in data:
                return JsonResponse({"error": f"Missing field: {field}"}, status=400)

        # Update fields
        resto_name = data.get('resto')
        try:
            restaurant = RumahMakan.objects.get(nama=resto_name)
            discount.resto = restaurant.nama
        except RumahMakan.DoesNotExist:
            return JsonResponse({"error": "Restaurant not found"}, status=400)
        
        discount.code = data.get('code')
        try:
            discount.percentage = float(data.get('percentage'))
            discount.min_payment = float(data.get('min_payment'))
        except ValueError:
            return JsonResponse({"error": "Invalid number format for percentage or min_payment"}, status=400)
        
        # Validate and parse date
        valid_period_str = data.get('valid_period')
        
        try:
            discount.valid_period = datetime.strptime(valid_period_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid date format for valid_period. Use YYYY-MM-DD."}, status=401)
        
        discount.save()

        return JsonResponse({"status": "success"}, status=200)

    return JsonResponse({"message": "Invalid request method"}, status=400)

@csrf_exempt
def delete_disc_entry_flutter(request, id):
    if request.method == 'POST':
        try:
            discount = DiscEntry.objects.get(pk=id)
            discount.delete()
            return JsonResponse({"status": True, "message": "Discount entry deleted successfully"}, status=200)
        except DiscEntry.DoesNotExist:
            return JsonResponse({"error": "Discount entry not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

def show_xml(request):
    data = DiscEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = DiscEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = DiscEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = DiscEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")