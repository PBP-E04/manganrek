from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_name', 'rumah_makan', 'stars', 'comments', 'visit_date']
