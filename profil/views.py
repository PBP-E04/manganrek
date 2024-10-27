from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.urls import reverse
from profil.models import UserProfile
from profil.forms import UserProfileForm, FoodPreferenceForm, SearchHistoryForm
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect  # Pastikan ini ada


@login_required(login_url='/login')
def show_main(request):
    profil, created = UserProfile.objects.get_or_create(user=request.user)
    context = {
        'name': profil.user.username,  # Ambil username dari User terkait
        'last_login': request.COOKIES.get('last_login', 'Tidak ada'),
        'profil': profil,
    }
    return render(request, "user_profile_list.html", context)

@login_required 
def user_profile_list(request):
    profil, created = UserProfile.objects.get_or_create(user=request.user)
    profiles = UserProfile.objects.filter(user=request.user)  # Hanya profil user yang login
    context = {'profiles': profiles}
    return render(request, 'user_profile_list.html', context)

@login_required 
def user_profile_detail(request, user_profile_id):
    user_profile = get_object_or_404(UserProfile, id=user_profile_id)
    is_following = request.user.profile.following.filter(id=user_profile.id).exists() if request.user.is_authenticated else False
    
    context = {
        'user_profile': user_profile,
        'is_following': is_following,
    }
    return render(request, 'user_profile_detail.html', context)

@login_required 
def user_profile_update(request, user_profile_id):
    user_profile = get_object_or_404(UserProfile, id=user_profile_id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profil:user_profile_detail', user_profile_id=user_profile.id)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'user_profile_update.html', {'form': form, 'user_profile': user_profile})

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

@login_required
def add_food_preference(request):
    if request.method == 'POST':
        form = FoodPreferenceForm(request.POST)
        if form.is_valid():
            food_preference = form.save(commit=False)
            food_preference.user_profile = UserProfile.objects.get(user=request.user)
            food_preference.save()
            return redirect('list_food_preferences')
    else:
        form = FoodPreferenceForm()
    return render(request, 'profil/add_food_preference.html', {'form': form})

def list_user_food_preferences(request):
    preferences = FoodPreference.objects.filter(user=request.user)  # Asumsi ada relasi dengan User
    return render(request, 'profil/list_food_preferences.html', {'preferences': preferences})

def add_search_history(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        # Logika untuk menyimpan search history
        SearchHistory.objects.create(user=request.user, query=search_query)
        return redirect('Add search history')  # Ubah dengan URL yang sesuai
    return render(request, 'profil/add_search_history.html')

def list_user_search_history(request):
    search_history = SearchHistory.objects.filter(user=request.user)
    return render(request, 'profil/search_history_list.html', {'search_history': search_history})


def register_user(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('login:user_profile_list')
    context = {'form':form}
    return render(request, 'register_user.html', context)

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
                response = redirect('profil:user_profile_list')  # Ganti sesuai URL yang benar
                response.set_cookie('last_login', str(datetime.datetime.now()))

                return response  
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('profil:login'))
    response.delete_cookie('last_login')
    return response

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profil:user_profile_list')  # Atau redirect ke profil pengguna

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profil:user_profile_list')  # Atau redirect ke profil pengguna

@login_required
def delete_account(request):
    if request.method == 'POST':
        # Logika untuk menghapus akun
        request.user.delete()
        messages.success(request, "Akun Anda telah berhasil dihapus.")
        return redirect('profil')  # Ganti 'home' dengan URL tujuan setelah penghapusan
    return render(request, 'profil/delete_account.html')