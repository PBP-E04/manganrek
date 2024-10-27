from django.db import models
import uuid

class RumahMakan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=50)
    alamat = models.CharField(max_length=255)
    tingkat_kepedasan = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    
class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_rumah_makan = models.ForeignKey(RumahMakan, on_delete=models.CASCADE)
    nama_makanan = models.CharField(max_length=50)
    harga = models.IntegerField()