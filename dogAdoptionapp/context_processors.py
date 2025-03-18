from .models import AdoptionRequest, Message

def notification_counts(request):
    pending_count = 0
    message_count = 0

    if request.user.is_authenticated:
        pending_count = AdoptionRequest.objects.filter(owner=request.user, status="Pending", seen=False).count()
        message_count = Message.objects.filter(recipient=request.user, is_read=False).count()

    return {
        "pending_requests_count": pending_count,
        "new_message_count": message_count,
    }
