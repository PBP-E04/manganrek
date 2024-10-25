from django.db import models
from django.contrib.auth.models import User
from datetime import date
from restoran_makanan.models import RumahMakan

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rumah_makan = models.ForeignKey(RumahMakan, on_delete=models.CASCADE) 
    review_name = models.CharField(max_length=100)
    stars = models.IntegerField()  # 1 to 5 stars
    comments = models.TextField()
    visit_date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.review_name} - {self.restaurant.name} ({self.stars} stars)"
