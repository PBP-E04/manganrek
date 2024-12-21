from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse,  HttpResponseNotAllowed
from .models import Review
from restoran_makanan.models import RumahMakan
from django.core import serializers 
from django.views.decorators.http import require_POST   
from .forms import ReviewForm
import json
from django.views.decorators.csrf import csrf_exempt


def review_list(request):
    query = request.GET.get('q', '')
    if query:
        reviews = Review.objects.filter(
            Q(review_name__icontains=query) |
            Q(rumah_makan__nama__icontains=query) |
            Q(comments__icontains=query)
        ).order_by('-created_at')
    else:
        reviews = Review.objects.all().order_by('-created_at')
    
    # Query all restaurants
    restaurants = RumahMakan.objects.all()

    context = {
        'reviews': reviews,
        'query': query,
        'restaurants': restaurants  # Add restaurants to the context
    }
    return render(request, 'review_list.html', context)


@login_required(login_url='/profil/login')
def add_review(request):
    if request.method == 'POST':
        review_name = request.POST.get('review_name')
        stars = request.POST.get('stars')
        comments = request.POST.get('comments')
        rumah_makan_id = request.POST.get('rumah_makan')
        visit_date = request.POST.get('visit_date')

        review = Review.objects.create(
            user=request.user,
            review_name=review_name,
            stars=stars,
            comments=comments,
            rumah_makan_id=rumah_makan_id,
            visit_date=visit_date
        )
        review.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# views.py
@login_required(login_url='/profil/login')
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'GET':
        restaurants = RumahMakan.objects.all()
        return render(request, 'edit_review_form.html', {'review': review, 'restaurants': restaurants})
    elif request.method == 'POST':
        # Process the form submission and update the review
        review.review_name = request.POST['review_name']
        review.rumah_makan = get_object_or_404(RumahMakan, pk=request.POST['rumah_makan'])
        review.stars = request.POST['stars']
        review.comments = request.POST['comments']
        review.visit_date = request.POST['visit_date']
        review.save()
        return redirect('review:review_list')

@require_POST
@login_required(login_url='/profil/login')
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    return JsonResponse({'success': True})


def show_json(request):
    data = Review.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_review_json(request, pk):
    try:
        resto = RumahMakan.objects.get(pk=pk)
        reviews = Review.objects.filter(rumah_makan=resto)
        return HttpResponse(serializers.serialize('json', reviews), content_type="application/json")
    except RumahMakan.DoesNotExist:
        return JsonResponse({'error': 'Restaurant not found'}, status=404)
    
@csrf_exempt
def create_review_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)

        # Assuming data is a list, extract the first dictionary object
        # review_data = data['rumah_makan']['fields']

        # Fetch RumahMakan instance using the UUID in 'rumah_makan'
        rumah_makan_instance = get_object_or_404(RumahMakan, pk=data["rumah_makan"]["pk"])

        # Create the Review object
        new_review = Review.objects.create(
            user=request.user,
            rumah_makan=rumah_makan_instance,
            review_name=data["review_name"],
            stars=data["stars"],
            comments=data["comments"],
            visit_date=data["visit_date"],
            created_at=data["created_at"],
        )

        return JsonResponse({
            "status": "success",
            "review_id": new_review.id
        }, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def delete_review_flutter(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=review_id)

        # Ensure the logged-in user can only delete their own reviews
        if review.user == request.user:
            review.delete()
            return JsonResponse({'success': True, 'message': 'Review deleted successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def update_review_flutter(request, review_id):
    if request.method == 'POST':
        try:
            review = Review.objects.get(pk=review_id)
            review.review_name = request.POST['review_name']
            review.comments = request.POST['comments']
            review.stars = int(request.POST['stars'])
            review.rumah_makan = RumahMakan.objects.get(pk=request.POST['rumah_makan'])
            review.visit_date = request.POST['visit_date']
            review.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})