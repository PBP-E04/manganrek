from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from restoran_makanan.models import RumahMakan, Menu
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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

@login_required(login_url='/profil/login')
def show_rumahmakan_makanan(request):
    rumah_makan = RumahMakan.objects.all()
    makanan = Menu.objects.all()
    
    context = {
        'rumah_makan': rumah_makan,
        'makanan': makanan,
    }
    return render(request, 'restoran_makanan.html', context)

@login_required(login_url='/profil/login')
def show_detail_rumah_makan(request, id_rumah_makan):
    rumah_makan = RumahMakan.objects.get(pk=id_rumah_makan)
    menu_items = Menu.objects.filter(id_rumah_makan=id_rumah_makan)
    context = {
        'rumah_makan': rumah_makan,
        'menu_items': menu_items,
    }
    return render(request, 'detail_rumah_makan.html', context)
    
@csrf_exempt
@require_POST
def add_rumah_makan(request):
    nama = request.POST.get('nama')
    alamat = request.POST.get('alamat')
    tingkat_kepedasan = request.POST.get('tingkat_kepedasan')
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')

    rumah_makan = RumahMakan(
        nama=nama,
        alamat=alamat,
        tingkat_kepedasan=tingkat_kepedasan,
        latitude=latitude,
        longitude=longitude
    )
    rumah_makan.save()

    return HttpResponse(b"CREATED", status=201)

@login_required(login_url='/profil/login')
def edit_rumah_makan(request, id):
    rumah_makan = get_object_or_404(RumahMakan, pk=id)
    if request.method == 'POST':
        rumah_makan.nama = request.POST.get('nama')
        rumah_makan.alamat = request.POST.get('alamat')
        rumah_makan.tingkat_kepedasan = request.POST.get('tingkat_kepedasan')
        rumah_makan.latitude = request.POST.get('latitude')
        rumah_makan.longitude = request.POST.get('longitude')
        rumah_makan.save()
        return redirect('restoran_makanan:show_rumahmakan_makanan')
    
    return render(request, 'edit_rumah_makan.html', {'rumah_makan': rumah_makan})

@login_required(login_url='/profil/login')
def delete_rumah_makan(request, id):
    rumah_makan = get_object_or_404(RumahMakan, pk=id)
    rumah_makan.delete()
    return HttpResponseRedirect(reverse('restoran_makanan:show_rumahmakan_makanan'))

@csrf_exempt
@require_POST
def add_menu(request, id_rumah_makan):
    rumah_makan = get_object_or_404(RumahMakan, pk=id_rumah_makan)
    nama_makanan = request.POST.get('nama_makanan')
    harga = request.POST.get('harga')

    menu = Menu(
        id_rumah_makan=rumah_makan,
        nama_makanan=nama_makanan,
        harga=harga
    )
    menu.save()

    return HttpResponse(b"CREATED", status=201)

@login_required(login_url='/profil/login')
def edit_menu(request, id):
    menu = get_object_or_404(Menu, pk=id)
    
    if request.method == 'POST':
        menu.nama_makanan = request.POST.get('nama_makanan')
        menu.harga = request.POST.get('harga')
        menu.save()
        return redirect('restoran_makanan:detail_rumah_makan', id_rumah_makan=menu.id_rumah_makan.id)
    
    context = {
        'menu': menu,
        'rumah_makan': menu.id_rumah_makan
    }
    return render(request, 'edit_menu.html', context)

@login_required(login_url='/profil/login')
def delete_menu(request, id):
    menu = get_object_or_404(Menu, pk=id)
    id_rumah_makan = menu.id_rumah_makan.id
    menu.delete()
    return HttpResponseRedirect(reverse('restoran_makanan:detail_rumah_makan', args=[id_rumah_makan]))