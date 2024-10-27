from django import forms
from .models import UserProfile, FoodPreference, SearchHistory

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [ 'email','foto_profil','jenis_makanan_favorit', 'preferensi_makanan']  # Sesuaikan dengan field di UserProfile

class FoodPreferenceForm(forms.ModelForm):
    class Meta:
        model = FoodPreference
        fields = ['name', 'description', 'rating', 'review']

class SearchHistoryForm(forms.ModelForm):
    class Meta:
        model = SearchHistory
        fields = ['search_term']
