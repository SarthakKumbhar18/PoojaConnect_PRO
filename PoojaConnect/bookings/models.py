from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from pandits.models import *


class Appointment(models.Model):
    STATUS_CHOICE = [('Pending','Pending'), ('Confirmed','Confirmed'), ('Cancelled','Cancelled'),]

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    pandit = models.ForeignKey(PanditProfile, on_delete = models.CASCADE)
    service = models.CharField(max_length = 100)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank = True)
    status = models.CharField(max_length = 20, choices = STATUS_CHOICE, default = 'Pending')
    created_at = models.DateTimeField(auto_now_add = True)
    

    def __str__(self):
        return f"{self.user.username} → {self.pandit.user.username}"
