import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from bookings.models import Appointment
from .models import VideoCall
from notifications.utils import notify

from django.conf import settings
from .utils import generate_zego_token


@login_required
def start_video_call(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    
    if request.user != appointment.pandit.user:
        return redirect("pandit_dashboard")

    
    if appointment.status != "Confirmed":
        return redirect("pandit_dashboard")

    
    call, created = VideoCall.objects.get_or_create(
        appointment=appointment,
        defaults={
            "room_name": str(uuid.uuid4()),
            "started_by": request.user
        }
    )

    
    notify(
        user=appointment.user,
        title="Incoming Video Call",
        message="Pandit has started a video call. Join now.",
        link=f"/video/join/{call.id}/",
        send_email=False
    )

    return redirect("join_video_call", call.id)


@login_required
@login_required
def join_video_call(request, call_id):
    call = get_object_or_404(VideoCall, id=call_id)

    if request.user not in [call.appointment.user, call.appointment.pandit.user]:
        return redirect("user_dashboard")

    is_pandit = request.user == call.appointment.pandit.user

    
    token = generate_zego_token(
    settings.ZEGO_APP_ID,
    settings.ZEGO_SERVER_SECRET,
    str(request.user.id)
)

    return render(request, "video/video_room.html", {
    "room_name": call.room_name,
    "app_id": settings.ZEGO_APP_ID,
    "server_secret": settings.ZEGO_SERVER_SECRET,
    "user_id": str(request.user.id),
    "user_name": request.user.username,
    "is_pandit": is_pandit,
})

