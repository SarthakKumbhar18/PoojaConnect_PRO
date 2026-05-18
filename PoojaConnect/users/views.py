from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *

from pandits.models import *
from bookings.forms import AppointmentForm
from bookings.models import *


from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from bookings.models import *

from payments.models import Payment

from notifications.utils import notify

from django.http import JsonResponse
from pandits.models import PanditProfile




def user_register(request):
    user_form = UserRegisterForm()
    profile_form = UserProfileForm()

    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "User registered successfully")
            return redirect('user_login')

    return render(
        request,
        'users/user_register.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )





def pandit_list(request):

    pandits = PanditProfile.objects.filter(verified=True)

    
    state = request.GET.get("state")
    city = request.GET.get("city")
    min_exp = request.GET.get("min_exp")
    max_fee = request.GET.get("max_fee")

    if state:
        pandits = pandits.filter(state__icontains=state)

    if city:
        pandits = pandits.filter(city__icontains=city)

    if min_exp:
        pandits = pandits.filter(experience__gte=min_exp)

    if max_fee:
        pandits = pandits.filter(fees__lte=max_fee)


    allowed_pandits = []

    if request.user.is_authenticated:
        allowed_pandits = Appointment.objects.filter(
            user=request.user
        ).values_list('pandit_id', flat=True)

    return render(request, 'users/pandit_list.html', {
        "pandits": pandits,
        "allowed_pandits": allowed_pandits
    })


def get_cities(request):
    state = request.GET.get("state")

    if state:
        cities = PanditProfile.objects.filter(
            verified=True,
            state__iexact=state
        ).values_list("city", flat=True).distinct().order_by("city")

        return JsonResponse(list(cities), safe=False)

    return JsonResponse([], safe=False)



@login_required
def book_appointment(request, pandit_id):
    pandit = PanditProfile.objects.get(id = pandit_id)

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save( commit = False)
            appointment.user = request.user
            appointment.pandit = pandit
            appointment.save()
            return redirect('user_dashboard')
        
    else:
        form = AppointmentForm()

    return render(request, 'users/book_appointment.html', {'form' : form, 'pandit' : pandit})



@login_required
def user_dashboard(request):
    appointments = Appointment.objects.filter(user = request.user).order_by("-created_at")
    return render(request, 'users/user_dashboard.html', {'appointments' : appointments})





@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id = appointment_id, user = request.user)

    if appointment.status != 'Pending':
        return HttpResponseForbidden("You cannot edit this appointment")
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance = appointment)

        if form.is_valid():
            form.save()

            notify(
            user=appointment.pandit.user,
            title="Appointment Updated",
            message=f"{request.user.username} updated the appointment details.",
            link="/pandits/dashboard/",
            )

            return redirect('user_dashboard')
        
    else:
        form = AppointmentForm(instance = appointment)

    return render(request, 'users/edit_appointment.html', {'form' : form})

        

@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id = appointment_id, user = request.user)

    if appointment.status != 'Pending':
        return HttpResponseForbidden("You cannot delete this appointment.")
    
    appointment.delete()
    return redirect('user_dashboard')



@login_required
def user_payments(request):
    payments = Payment.objects.filter(
        appointment__user=request.user
    )
    return render(request, 'payments/user_payments.html', {'payments': payments})


