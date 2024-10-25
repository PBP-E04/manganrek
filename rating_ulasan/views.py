from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from restoran_makanan.models import RumahMakan  # Import the RumahMakan model
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden

#pre
# @login_required
# def review_page(request, rumah_makan_nama):
#     # Simulate logging in as the regular user created earlier
#     user = get_object_or_404(User, username='regularuser')
#     login(request, user)  # Logs in the user for the session

#     # Now proceed with the usual logic to handle reviews
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.user = user  # Attach the logged-in user to the review
#             review.rumah_makan = get_object_or_404(RumahMakan, nama=rumah_makan_nama)
#             review.save()
#             return redirect('review_page', rumah_makan_nama=rumah_makan_nama)
#     else:
#         form = ReviewForm()

#     # Load existing reviews for display
#     reviews = Review.objects.filter(rumah_makan__nama=rumah_makan_nama)
    
#     return render(request, 'review_form.html', {
#         'form': form,
#         'reviews': reviews,
#         'rumah_makan': get_object_or_404(RumahMakan, nama=rumah_makan_nama),
#     })

#yatta bisa 
def review_page(request, rumah_makan_nama):
    # Simulate logging in as the regular user created earlier
    user = get_object_or_404(User, username='regularuser')
    login(request, user)  # Logs in the user for the session
    rumah_makan_nama = rumah_makan_nama.replace('-', ' ')

    # Now proceed with the usual logic to handle reviews
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = user  # Attach the logged-in user to the review
            review.rumah_makan = get_object_or_404(RumahMakan, nama=rumah_makan_nama)
            review.save()
            return redirect('review_page', rumah_makan_nama=rumah_makan_nama)
    else:
        form = ReviewForm()

    # Load existing reviews for display
    reviews = Review.objects.filter(rumah_makan__nama=rumah_makan_nama)
    
    return render(request, 'review_form.html', {
        'form': form,
        'reviews': reviews,
        'rumah_makan': get_object_or_404(RumahMakan, nama=rumah_makan_nama),
    })


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