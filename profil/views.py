from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.urls import reverse
from profil.models import UserProfile, Follower
from django.contrib.auth.models import User
from profil.forms import UserProfileForm
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@login_required(login_url='/profil/login')
def show_main(request):
    profil, created = UserProfile.objects.get_or_create(user=request.user)
    context = {
        'name': profil.user.username,  # Ambil username dari User terkait
        'last_login': request.COOKIES.get('last_login', 'Tidak ada'),
        'profil': profil,
    }
    return render(request, "user_profile_list.html", context)

@login_required(login_url='/profil/login')
def user_profile_list(request):
    profiles = UserProfile.objects.all()  # Hanya profil user yang login
    context = {'profiles': profiles}
    return render(request, 'user_profile_list.html', context)

@login_required(login_url='/profil/login')
def user_profile_detail(request, user_profile_id):
    user_profile = get_object_or_404(UserProfile, id=user_profile_id)
    is_following = Follower.objects.filter(
        follower=request.user.profile,
        user=user_profile
    ).exists()
    
    context = {
        'user_profile': user_profile,
        'is_following': is_following,
    }
    return render(request, 'user_profile_detail.html', context)

@login_required(login_url='/profil/login')
def user_profile_update(request, user_profile_id):
    user_profile = get_object_or_404(UserProfile, id=user_profile_id)
    
    if user_profile.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this profile")
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            # Handle file upload
            if form.cleaned_data.get('email'):
                user_profile.user.email = form.cleaned_data['email']
                user_profile.user.save()
                
            if 'foto_profil' in request.FILES:
                user_profile.foto_profil = request.FILES['foto_profil']
            profile = form.save()
            return redirect('profil:user_profile_detail', user_profile_id=user_profile.id)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'user_profile_update.html', {
        'form': form,
        'user_profile': user_profile
    })
    
def user_profile_create(request):
    """Create a new user profile."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile_list')  # Redirect ke daftar profil setelah berhasil
    else:
        form = UserProfileForm()
    
    return render(request, 'user_profile_form.html', {'form': form})

def user_profile_delete(request, user_id):
    """Delete a user's profile."""
    user_profile = get_object_or_404(UserProfile, id=user_id)
    if request.method == 'POST':
        user_profile.delete()
        return redirect('user_profile_list')  # Redirect ke halaman daftar setelah penghapusan
    return render(request, 'user_profile_confirm_delete.html', {'user_profile': user_profile})
    
@csrf_exempt
def register_user(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, 'Your account has been successfully created!')
            return redirect('profil:login')
    context = {'form':form}
    return render(request, 'register_user.html', context)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Buat response baru
                response = redirect('main:show_main')  # Ganti sesuai URL yang benar
                response.set_cookie('last_login', str(datetime.datetime.now()))

                return response  
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@csrf_exempt
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('profil:login'))
    response.delete_cookie('last_login')
    return response

@login_required(login_url='/profil/login')
def follow_user(request, user_profile_id):
    profile_to_follow = get_object_or_404(UserProfile, id=user_profile_id)
    Follower.objects.get_or_create(follower=request.user.profile, user=profile_to_follow)
    context = {
        'user_profile': profile_to_follow,
        'is_following': True  # We know it's true because we just followed
    }
    return render(request, 'user_profile_detail.html', context)

@login_required(login_url='/profil/login')
def unfollow_user(request, user_profile_id):
    profile_to_unfollow = get_object_or_404(UserProfile, id=user_profile_id)
    Follower.objects.filter(follower=request.user.profile, user=profile_to_unfollow).delete()
    context = {
        'user_profile': profile_to_unfollow,
        'is_following': False  # We know it's false because we just unfollowed
    }
    return render(request, 'user_profile_detail.html', context)

@login_required(login_url='/profil/login')
def delete_account(request):
    if request.method == 'POST':
        # Logika untuk menghapus akun
        request.user.delete()
        messages.success(request, "Akun Anda telah berhasil dihapus.")
        return redirect('main:show_main')  # Ganti 'home' dengan URL tujuan setelah penghapusan
    return render(request, 'delete_account.html')

@csrf_exempt
def login_flutter(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!",
                "id": user.id,
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)

@csrf_exempt
def register_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
            
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        user_profile = UserProfile.objects.create(user=user)
        user_profile.save()
        
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!",
            "id": user.id,
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)
        
@csrf_exempt
def logout_flutter(request):
    try:
        logout(request)
        return JsonResponse({
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
            "status": False,
            "message": "Logout gagal."
        }, status=401)
        
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all().values('id', 'username')
        return JsonResponse(list(users), safe=False, status=200)
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)