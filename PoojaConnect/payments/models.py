from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from bookings.models import Appointment



class Invoice(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete = models.CASCADE, related_name = 'invoice')
    base_fee = models.DecimalField(max_digits = 8, decimal_places = 2)
    pooja_samagri_fee = models.DecimalField(max_digits = 8, decimal_places = 2, default = 0.00)
    miscellaneous_fee = models.DecimalField(max_digits = 8, decimal_places = 2, default = 0.00)

    total_amount = models.DecimalField(max_digits = 8, decimal_places = 2)

    created_at = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return f"Invoice {self.id} - {self.total_amount}"



class Payment(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete = models.CASCADE)
    invoice = models.OneToOneField('Invoice', on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    pandit = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'pandit_payments', null = True)

    razorpay_order_id = models.CharField(max_length = 100, null = True)
    razorpay_payment_id = models.CharField(max_length = 100, blank = True, null = True)
    razorpay_signature = models.CharField(max_length = 100, blank = True, null = True)

    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    status = models.CharField(max_length = 20, choices = [('Created', 'Created'),('Paid', 'Paid'),('Failed', 'Failed')], default = 'Created')

    created_at = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"



