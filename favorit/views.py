from django.contrib.auth.decorators import login_required
from favorit.models import RumahMakanFavorit
from restoran_makanan.models import RumahMakan, Menu
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.urls import reverse
import uuid
import json

# Create your views here.
@login_required(login_url='/profil/login')
def show_favorit(request):
    return render(request, "show_favorit.html")

def show_json_favorit(request):
    data = RumahMakanFavorit.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_rumah_makan_by_favorit(request, id_rumah_makan):
    data = RumahMakanFavorit.objects.filter(id_rumah_makan=id_rumah_makan)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def update_favorit_restoran(request, id):
    # Get all interactions for the user and mood entry
    rumahmakan_favorit_obj = RumahMakanFavorit.objects.filter(user=request.user, id_rumah_makan_id=id)

    # If there are no interactions, create one
    if not rumahmakan_favorit_obj.exists():
        rumahmakan_favorit = RumahMakanFavorit.objects.create(user=request.user, id_rumah_makan_id=id)
    else:
        rumahmakan_favorit = rumahmakan_favorit_obj.first()

    rumahmakan_favorit.favorit = not rumahmakan_favorit.favorit  # Toggle favourite
    rumahmakan_favorit.save()
    return HttpResponseRedirect(reverse('restoran_makanan:show_rumahmakan_makanan'))

def update_favorit_favorit(request, id):
    # Get all interactions for the user and mood entry
    restoran_favorit_obj = RumahMakanFavorit.objects.filter(user=request.user, id_rumah_makan_id=id)

    # If there are no interactions, create one
    if not restoran_favorit_obj.exists():
        restoran_favorit = RumahMakanFavorit.objects.create(user=request.user, id_rumah_makan_id=id)
    else:
        restoran_favorit = restoran_favorit_obj.first()

    restoran_favorit.favorit = not restoran_favorit.favorit  # Toggle favourite
    restoran_favorit.save()
    return HttpResponseRedirect(reverse('favorit:show_favorit'))