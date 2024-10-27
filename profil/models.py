from django.db import models
import uuid 
from django.contrib.auth.models import User 

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    foto_profil = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='profile_pics/default.png')
    jenis_makanan_favorit = models.CharField(max_length=255, blank=True, null=True)
    preferensi_makanan = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    @property
    def foto_profil_url(self):
        if self.foto_profil and hasattr(self.foto_profil, 'url'):
            return self.foto_profil.url
        return None

class Follower(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.follower.nama} mengikuti {self.user.nama}"