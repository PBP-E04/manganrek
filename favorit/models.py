from django.contrib.auth.models import User
from django.db import models
import uuid
from restoran_makanan.models import RumahMakan
# Create your models here.

class RumahMakanFavorit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_rumah_makan = models.ForeignKey(RumahMakan, on_delete=models.CASCADE)
    favorit = models.BooleanField(default=False)