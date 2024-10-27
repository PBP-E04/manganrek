from django import forms
from .models import DiscEntry
from restoran_makanan.models import RumahMakan

class DiscEntryForm(forms.ModelForm):
    # Add a CharField for restaurant name input
    resto = forms.ModelChoiceField(
        queryset=RumahMakan.objects.all(),
        to_field_name="nama",  # Use restaurant name instead of UUID
        label="Restaurant",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select Restaurant'
        })
    )

    class Meta:
        model = DiscEntry
        fields = ['code', 'resto', 'percentage', 'min_payment', 'valid_period']
        widgets = {
            'valid_period': forms.SelectDateWidget(),
        }