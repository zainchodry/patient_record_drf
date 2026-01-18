from .models import Notification
from .email_service import send_notification_email

def create_notification(
    user,
    title,
    message,
    notification_type='system',
    send_email=True
):
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type
    )

    if send_email and user.email:
        send_notification_email(
            to_email=user.email,
            subject=title,
            message=message
        )
        notification.email_sent = True
        notification.save(update_fields=['email_sent'])

    return notification
