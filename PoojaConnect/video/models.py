from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from bookings.models import Appointment

class VideoCall(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=200)
    started_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"VideoCall - {self.room_name}"