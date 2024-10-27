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


@require_http_methods(["GET"])
def search_promos(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        # Search in both voucher codes and restaurant names
        disc_entries = DiscEntry.objects.filter(
            Q(code__icontains=query) |
            Q(resto__icontains=query)
        )
    else:
        disc_entries = DiscEntry.objects.all()
    
    # Serialize the results
    serialized_data = serializers.serialize('json', disc_entries)
    return JsonResponse({'results': serialized_data}, safe=False)


# Create your views here.
def show_main(request):
    disc_entries = DiscEntry.objects.all()
    restaurants = RumahMakan.objects.all()
    context = {
        'disc_entries': disc_entries,
        'restaurants': restaurants
    }
    return render(request, "promo_main.html", context)

def create_disc_entry(request):
    form = DiscEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('promo_diskon:show_main')

    context = {'form': form}
    return render(request, "create_disc_entry.html", context)

@csrf_exempt
@require_POST
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

    form_data = {field.name: form[field.name].value() for field in form}
    context = {
        'form': form,
        'form_data': form_data,  # Get restaurant name
        'resto_name': resto_name
    }
    return render(request, "edit_disc.html", context)
    

def delete_disc(request, id):
    # Get product berdasarkan id
    disc = DiscEntry.objects.get(pk = id)
    # Hapus product
    disc.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('promo_diskon:show_main'))

@require_http_methods(["GET"])
def search_promos(request):
    query = request.GET.get('q', '')
    
    if query:
        # Search in both voucher codes and restaurant names
        disc_entries = DiscEntry.objects.filter(
            Q(kode_voucher__icontains=query) |
            Q(resto__icontains=query)
        )
    else:
        disc_entries = DiscEntry.objects.all()
    
    # Serialize the results
    data = serializers.serialize('json', disc_entries)
    return JsonResponse({'results': data}, safe=False)

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