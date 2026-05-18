from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class PanditProfile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    photo = models.ImageField(upload_to = 'pandits/',default="")
    state = models.CharField(max_length = 50)
    city = models.CharField(max_length = 50)
    experience = models.IntegerField()
    expertise = models.CharField(max_length = 200)
    fees = models.DecimalField(max_digits = 10, decimal_places = 2)
    verified = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username 