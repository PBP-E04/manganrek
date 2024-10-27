from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False)  # Add email field

    class Meta:
        model = UserProfile
        fields = ['foto_profil', 'jenis_makanan_favorit', 'preferensi_makanan']
        widgets = {
            'foto_profil': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
