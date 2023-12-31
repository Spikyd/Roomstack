from django.db.models import OuterRef, Subquery

from roommate.models import UserProfile, Apartment, Message


def navbar_data(request):
    context = {}
    if request.user.is_authenticated:
        context['user_profile'] = UserProfile.objects.filter(user=request.user).first()
    return context


def user_has_posted_room(request):
    user = request.user
    user_apartment = None
    if user.is_authenticated:
        user_apartment = Apartment.objects.filter(author=user).first()
    return {'user_apartment': user_apartment}


def unread_message_count(request):
    if request.user.is_authenticated:
        latest_messages = Message.objects.filter(receiver=request.user, is_read=False,
                                                 sender=OuterRef('sender')).order_by('-timestamp')
        unread_count = Message.objects.filter(receiver=request.user, is_read=False,
                                              timestamp=Subquery(latest_messages.values('timestamp')[:1])).count()
    else:
        unread_count = 0

    return {'unread_message_count': unread_count}
