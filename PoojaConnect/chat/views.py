from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import *

from django.db.models import Q, Max


@login_required
def chat_list(request):
    chats = ChatRoom.objects.filter(
        models.Q(user=request.user) | models.Q(pandit=request.user)
    )

    chat_data = []
    for chat in chats:
        chat_data.append({
            "chat": chat,
            "unread_count": chat.unread_count_for(request.user)
        })

    is_pandit = hasattr(request.user, "panditprofile")

    return render(request, "chat/chat_list.html", {
        "chat_data": chat_data,
        "is_pandit": is_pandit
    })



@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    print(type(room.pandit))

    
    if request.user not in [room.user, room.pandit]:
        return HttpResponse("Unauthorized", status=403)

    
    if room.appointment.status != "Confirmed":
        return HttpResponse("Chat available only for confirmed appointments.", status=403)

    
    room.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    if request.method == "POST":
        Message.objects.create(room=room,sender=request.user,text=request.POST.get("message"),attachment=request.FILES.get("attachment"))
        return redirect("chat_room", room_id=room.id)

    messages = room.messages.all().order_by("timestamp")

    return render(request, "chat/chat_room.html", {
        "room": room,
        "messages": messages
    })






@login_required
def start_chat(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    
    if appointment.user != request.user:
        return HttpResponse("Unauthorized", status=403)

    if appointment.status != 'Confirmed':
        return HttpResponse("Chat allowed only after confirmation", status=403)

    
    room, created = ChatRoom.objects.get_or_create(
        appointment=appointment,
        defaults={
            'user': appointment.user,
            'pandit': appointment.pandit.user
        }
    )

    return redirect('chat_room', room.id)