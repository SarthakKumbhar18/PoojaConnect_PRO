from django.http import HttpResponse
from django.shortcuts import render,redirect

# Create your views here.


def home_view(request):
    return render(request,'home/PoojaConnectHome.html')

def astrology_view(request):
    return render(request,'home/astrology.html')

def astro_horoscope_view(request):
    return render(request,'home/astro_horoscope.html')

def astro_kundli_view(request):
    return render(request,'home/astro_kundli.html')

def astro_panchang_view(request):
    return render(request,'home/astro_panchang.html')

def astro_grahadasha_view(request):
    return render(request,'home/astro_grahadasha.html')

def astro_numerology_view(request):
    return render(request,'home/astro_numerology.html')

def astro_gems_view(request):
    return render(request,'home/astro_gems.html')




def temples_view(request):
    return render(request,'home/temple.html')

def temples_karnataka_view(request):
    return render(request,'home/temple_karnataka.html')

def temples_maharashtra_view(request):
    return render(request,'home/temple_maharashtra.html')

def temples_tamilnadu_view(request):
    return render(request,'home/temple_tamilnadu.html')

def temples_uttrakhand_view(request):
    return render(request,'home/temple_uttrakhand.html')




def puja_view(request):
    return render(request,'home/puja.html')

def puja_satyanarayan_view(request):
    return render(request,'home/puja_satyanarayan.html')

def puja_ganesh_view(request):
    return render(request,'home/puja_ganesh.html')

def puja_rudrabhishek_view(request):
    return render(request,'home/puja_rudrabhishek.html')

def puja_laxmi_view(request):
    return render(request,'home/puja_laxmi.html')

def puja_hanuman_view(request):
    return render(request,'home/puja_hanuman.html')

def puja_durga_view(request):
    return render(request,'home/puja_durga.html')

def puja_saraswati_view(request):
    return render(request,'home/puja_saraswati.html')





def library_view(request):
    return render(request,'home/library.html')



def help_view(request):
    return render(request,'home/help_page.html')