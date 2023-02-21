from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from roommate.forms import RoomForm, ContactForm
from roommate.models import Roommate, Room


class HomeTemplateView(TemplateView):
    template_name = 'home_page.html'


class BrowseRoommatesView(ListView):
    model = Roommate
    template_name = 'browse_roommates.html'
    context_object_name = 'roommates'


class RoomDetailView(DetailView):
    model = Room
    template_name = 'room_detail.html'
    context_object_name = 'room'


class PostARoomView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'post_a_room.html'
    success_url = reverse_lazy('room_list')


class ContactUsView(CreateView):
    template_name = 'contact_us.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        send_mail(
            'Contact Form Submission',
            f'Name: {name}\nEmail: {email}\nMessage: {message}',
            'info@findaroommate.com',
            ['admin@findaroommate.com'],
            fail_silently=False,
        )
        return super().form_valid(form)
