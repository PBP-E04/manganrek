from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseRedirect
from django.core import serializers
import json
from promo_diskon.models import DiscEntry
from promo_diskon.forms import DiscEntryForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

# Create your views here.
def show_main(request):
    disc_entries = DiscEntry.objects.all()
    context = {'disc_entries': disc_entries}
    return render(request, "main.html", context)

def create_disc_entry(request):
    form = DiscEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('promo_diskon:show_main')

    context = {'form': form}
    return render(request, "create_disc_entry.html", context)

# @login_required
@require_POST
def add_disc_entry_ajax(request):
    form = DiscEntryForm(request.POST)
    
    if form.is_valid():
        disc = form.save(commit=False)
        disc.user = request.user  # Set the current logged-in user
        disc.save()  # Save the form
        return JsonResponse({"message": "CREATED"}, status=201)
    else:
        errors = form.errors.as_json()
        return JsonResponse({"error": errors}, status=400)



def edit_disc_info(request, id):
    # Get product entry berdasarkan id
    disc = DiscEntry.objects.get(pk = id)

    # Set product entry sebagai instance dari form
    form = DiscEntryForm(request.POST or None, instance=disc)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('promo_diskon:show_main'))

    context = {'form': form}
    return render(request, "edit_disc.html", context)

def delete_disc(request, id):
    # Get product berdasarkan id
    disc = DiscEntry.objects.get(pk = id)
    # Hapus product
    disc.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('promo_diskon:show_main'))
    

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