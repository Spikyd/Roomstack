from roommate.models import UserProfile, Apartment


def navbar_data(request):
    context = {}
    if request.user.is_authenticated:
        context['user_profile'] = UserProfile.objects.filter(user=request.user).first()
    return context


def user_has_posted_room(request):
    user = request.user
    has_posted_room = False
    if user.is_authenticated:
        has_posted_room = Apartment.objects.filter(author=user).exists()
    return {'user_has_posted_room': has_posted_room}
