import csv
from django.shortcuts import render
from django.http import HttpResponse
from .models import RumahMakan, Menu
from django.core import serializers

def show_json_rumah_makan(request):
    data = RumahMakan.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_rumah_makan_by_id(request, id):
    data = RumahMakan.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_menu(request):
    data = Menu.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_menu_by_id(request, id):
    data = Menu.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_menu_by_rumah_makan(request, id_rumah_makan):
    data = Menu.objects.filter(id_rumah_makan=id_rumah_makan)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")