from django.db import models
import uuid
from django.contrib.auth.models import User
from restoran_makanan.models import RumahMakan

# Create your models here.
class DiscEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    # resto = models.ForeignKey(RumahMakan, on_delete=models.CASCADE)
    percentage = models.IntegerField()
    min_payment = models.IntegerField()
    valid_period = models.DateField()  # Changed to DateField