from django import forms
from .models import DiscEntry

class DiscEntryForm(forms.ModelForm):
    class Meta:
        model = DiscEntry
        fields = ['code', 'percentage', 'min_payment', 'valid_period']
