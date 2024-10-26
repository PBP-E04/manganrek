from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from restoran_makanan.models import RumahMakan  # Import the RumahMakan model
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from itertools import chain
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
#pre
@login_required
def review_page(request, rumah_makan_nama):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user 
            review.rumah_makan = get_object_or_404(RumahMakan, nama=rumah_makan_nama)
            review.save()
            return redirect('review_page', rumah_makan_nama=rumah_makan_nama)
    else:
        form = ReviewForm()

    reviews = Review.objects.filter(rumah_makan__nama=rumah_makan_nama)
    
    return render(request, 'review_form.html', {
        'form': form,
        'reviews': reviews,
        'rumah_makan': get_object_or_404(RumahMakan, nama=rumah_makan_nama),
    })

# @login_required
# def show_review_page(request):
#     # Fetch all restaurants to display on the main page
#     restaurants = RumahMakan.objects.all()
#     return render(request, 'restaurant_list.html', {'restaurants': restaurants})

@login_required
def show_review_page(request):
    resto = RumahMakan.objects.all()
    context = {
        'restaurants': resto
    }
    return render(request, "review_page.html", context)

def search_restaurants(request):
    search_term = request.GET.get('q', '')
    data = []

    if search_term:
        # Filter restaurants by name containing the search term
        restaurants = RumahMakan.objects.filter(nama__icontains=search_term)
        data = list(restaurants)  # Prepare the queryset for serialization

    # Return serialized JSON data with application/json content type
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

#better use async 
@login_required
def delete_review(request, restaurant_name, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.user or request.user.is_superuser:  # Check if user is owner or admin
        review.delete()
        return redirect(f'/restaurant-name/review-page/')
    else:
        return HttpResponseForbidden("You are not allowed to delete this review.")


def edit_review(request, rumah_makan_nama, review_id):
    # Fetch the review by ID
    review = get_object_or_404(Review, id=review_id)
    
    # Check if the user is allowed to edit the review (e.g., the owner of the review)
    if request.user != review.user:
        return redirect('some_error_page')  # Redirect or show an error message
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_page', rumah_makan_nama=rumah_makan_nama)  # Redirect to the review page
    else:
        form = ReviewForm(instance=review)  # Pre-populate the form with the current review data
    
    return render(request, 'rating_ulasan/edit_review.html', {'form': form, 'rumah_makan_nama': rumah_makan_nama, 'review': review})

# ini buat yang ada di profile resto
@login_required
def show_review(request, rumah_makan_nama):
    # Get the specific restaurant (RumahMakan) based on the 'nama'
    rumah_makan = get_object_or_404(RumahMakan, nama=rumah_makan_nama)
    
    # Fetch all reviews for this specific restaurant
    reviews = Review.objects.filter(rumah_makan=rumah_makan)
    
    # Render the reviews to the template
    return render(request, 'rating_ulasan/show_review.html', {
        'rumah_makan': rumah_makan,
        'reviews': reviews
    })


def show_json(request):
    data = Review.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_review_json(request, pk):
    resto = RumahMakan.objects.get(pk=pk)
    reviews = Review.objects.filter(r=resto)
    return HttpResponse(serializers.serialize('json', reviews), content_type="application/json")