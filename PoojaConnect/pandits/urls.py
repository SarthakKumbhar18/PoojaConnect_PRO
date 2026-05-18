from django.urls import path,include
from .views import*
urlpatterns = [
    path('dashboard/', pandit_dashboard,name = 'pandit_dashboard'),
    path('register/', pandit_register, name = 'pandit_register'),
    path('accept/<int:appointment_id>', accept_appointment, name = 'accept_appointment'),
    path('reject/<int:appointment_id>', reject_appointment, name = 'reject_appointment'),
]
