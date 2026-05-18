from .models import Notification
from django.core.mail import send_mail
from django.conf import settings


def notify(user, title, message, link=None, send_email=False):
    """
    Create in-app notification
    Optionally send email
    """

    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        link=link
    )

    if send_email and user.email:
        send_mail(
            subject=title,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True
        )


def unread_count(user):
    return Notification.objects.filter(user=user, is_read=False).count()