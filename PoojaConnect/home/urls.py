from django.urls import path
from .views import *


urlpatterns = [

    
    path('', home_view, name = 'home'),

    
    path('astrology/', astrology_view, name = 'astrology'),
    path('astro_horoscope/', astro_horoscope_view, name = 'astro_horoscope'),
    path('astro_kundli/', astro_kundli_view, name = 'astro_kundli'),
    path('astro_panchang/', astro_panchang_view, name = 'astro_panchang'),
    path('astro_grahadasha/', astro_grahadasha_view, name = 'astro_grahadasha'),
    path('astro_numerology/', astro_numerology_view, name = 'astro_numerology'),
    path('astro_gems/', astro_gems_view, name = 'astro_gems'),


    
    path('temples/', temples_view, name = 'temples'),
    path('temples_karnataka/', temples_karnataka_view, name = 'temples_karnataka'),
    path('temples_maharashtra/', temples_maharashtra_view, name = 'temples_maharashtra'),
    path('temples_tamilnadu/', temples_tamilnadu_view, name = 'temples_tamilnadu'),
    path('temples_uttrakhand/', temples_uttrakhand_view, name = 'temples_uttrakhand'),



    
    path('puja/', puja_view, name = 'puja'),
    path('puja_satyanarayan/', puja_satyanarayan_view, name = 'puja_satyanarayan'),
    path('puja_ganesh/', puja_ganesh_view, name = 'puja_ganesh'),
    path('puja_rudrabhishek/', puja_rudrabhishek_view, name = 'puja_rudrabhishek'),
    path('puja_laxmi/', puja_laxmi_view, name = 'puja_laxmi'),
    path('puja_hanuman/', puja_hanuman_view, name = 'puja_hanuman'),
    path('puja_durga/', puja_durga_view, name = 'puja_durga'),
    path('puja_saraswati/', puja_saraswati_view, name = 'puja_saraswati'),


    
    path('library/', library_view, name = 'library'),


    
    
    path('help/', help_view, name = 'help'),


    
]