from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from .models import Notification

# Create your views here.


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)

    notifications.filter(is_read=False).update(is_read=True)

    
    is_pandit = hasattr(request.user, "panditprofile")

    return render(request, "notifications/list.html", {
        "notifications": notifications.order_by("-created_at"),
        "is_pandit": is_pandit
    })