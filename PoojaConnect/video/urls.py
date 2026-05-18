from django.urls import path
from .views import start_video_call, join_video_call

urlpatterns = [
    path('start/<int:appointment_id>/', start_video_call, name='start_video_call'),
    path('join/<int:call_id>/', join_video_call, name='join_video_call'),
]