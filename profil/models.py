from django.db import models
import uuid 
from django.contrib.auth.models import User 

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(unique=True)
    foto_profil = models.ImageField(upload_to='profil_pictures/', blank=True, null=True)
    jenis_makanan_favorit = models.CharField(max_length=255, blank=True, null=True)
    preferensi_makanan = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Follower(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.follower.nama} mengikuti {self.user.nama}"

class FoodPreference(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='food_preferences')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=0, choices=[(i, str(i)) for i in range(1, 6)])  # Rating 1-5
    review = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class SearchHistory(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='search_history')
    search_term = models.CharField(max_length=255)
    search_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.search_term

