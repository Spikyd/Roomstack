from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from roommate.forms import MessageForm
from roommate.models import Apartment, Favorite, UserProfile


class HomeTemplateView(TemplateView):
    template_name = 'home_page.html'


@login_required
def add_favorite(request, room_id):
    room = get_object_or_404(Apartment, id=room_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, room=room)
    return redirect('room_detail', room_id=room.id)


@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorite_list.html', {'favorites': favorites})

@login_required
def compose_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = Message(sender=request.user, receiver=receiver, message=form.cleaned_data['message'])
            message.save()
            sender_profile = UserProfile.objects.get(user=request.user)
            receiver_profile = UserProfile.objects.get(user=receiver)
            sender_profile.messages.add(message)
            receiver_profile.messages.add(message)
            return redirect('profile', username=receiver.username)
    return render(request, 'compose_message.html', {'receiver': receiver, 'form': form})