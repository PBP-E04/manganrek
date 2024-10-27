from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse,  HttpResponseNotAllowed
from .models import Review
from restoran_makanan.models import RumahMakan
from django.core import serializers 
from django.views.decorators.http import require_POST   

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


@login_required
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

@login_required
def edit_review(request, review_id):
    if request.method == 'GET':
        try:
            review = Review.objects.get(id=review_id)
            data = {
                'success': True,
                'review_name': review.review_name,
                'rumah_makan_id': review.rumah_makan.id,
                'stars': review.stars,
                'comments': review.comments,
                'visit_date': review.visit_date.strftime('%Y-%m-%d'),
            }
            return JsonResponse(data)
        except Review.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Review not found'})
    return HttpResponseNotAllowed(['GET'])

@require_POST
@login_required
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