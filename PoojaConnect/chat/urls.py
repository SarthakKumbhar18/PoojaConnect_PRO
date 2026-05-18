from django.urls import path
from .views import *




urlpatterns = [
    path('', chat_list, name='chat_list'),
    path('<int:room_id>/', chat_room, name='chat_room'),
    path('start/<int:appointment_id>/', start_chat, name='start_chat'),
]