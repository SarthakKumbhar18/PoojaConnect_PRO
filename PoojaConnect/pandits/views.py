from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.contrib import messages
from .forms import *
from bookings.models import *

from payments.models import Payment
from notifications.utils import notify



def pandit_register(request):

    user_form = PanditRegisterForm()
    profile_form = PanditProfileForm()

    if request.method == "POST":
        user_form = PanditRegisterForm(request.POST)
        profile_form = PanditProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request,"Pandit registered successfully. Please login.")
            return redirect('pandit_login')
        
    
    return render(request, 'pandits/pandit_register.html',{
        'user_form': user_form,
        'profile_form': profile_form
    })



@login_required
def pandit_dashboard(request):
    pandit = request.user.panditprofile
    appointments = Appointment.objects.filter(pandit = pandit).order_by("-created_at")

    return render(request, 'pandits/pandit_dashboard.html', {'appointments':appointments})


@login_required
def accept_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id = appointment_id)
    appointment.status = 'Confirmed'
    appointment.save()

    notify(
        user=appointment.user,
        title="Appointment Confirmed",
        message=f"Your appointment with Pandit {request.user.username} has been confirmed.",
        link="/users/dashboard/",
        send_email=True
    )

    return redirect('pandit_dashboard')


@login_required
def reject_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id = appointment_id)
    appointment.status = 'Cancelled'
    appointment.save()

    notify(
        user=appointment.user,
        title="Appointment Rejected",
        message=f"Your appointment with Pandit {request.user.username} was rejected.",
        link="/users/dashboard/",
        send_email=True
    )
    
    return redirect('pandit_dashboard')


@login_required
def pandit_payments(request):
    payments = Payment.objects.filter(
        appointment__pandit__user=request.user,
        status='Success'
    )
    return render(request, 'payments/pandit_payments.html', {'payments': payments})



