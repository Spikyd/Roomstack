from roommate.models import UserProfile
from django.conf import settings


def navbar_data(request):
    context = {}
    if request.user.is_authenticated:
        context['user_profile'] = UserProfile.objects.filter(user=request.user).first()
    return context

