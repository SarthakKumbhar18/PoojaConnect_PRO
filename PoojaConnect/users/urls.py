from django.urls import path,include
from .views import*
urlpatterns = [
    path('dashboard/', user_dashboard, name = 'user_dashboard'),
    path('register/', user_register, name = 'user_register'),
    path('pandits/', pandit_list, name = 'pandit_list'),
    path('book/<int:pandit_id>', book_appointment, name = 'book_appointment'),
    path('appointment/edit/<int:appointment_id>/', edit_appointment, name = 'edit_appointment'),
    path('appointment/delete/<int:appointment_id>/', delete_appointment, name = 'delete_appointment'),

    path('ajax/get-cities/', get_cities, name='get_cities'),
]