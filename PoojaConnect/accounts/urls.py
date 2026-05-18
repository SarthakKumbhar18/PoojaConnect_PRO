from django.urls import path
from .views import *


urlpatterns = [

    path('user/login/',user_login, name = 'user_login'),
    path('pandit/login/',pandit_login, name = 'pandit_login'),
    path('user_logout/',user_logout_view, name = 'user_logout'),
    path('pandit_logout/',pandit_logout_view, name = 'pandit_logout'),

    
]