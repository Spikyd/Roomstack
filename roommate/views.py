from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView, DetailView

from roommate.forms import UserRegisterForm, UserProfileForm, ApartmentForm, AuthenticationNewForm
from roommate.models import Apartment, UserProfile, Favorite, ApartmentImage


class HomeTemplateView(TemplateView):
    template_name = 'home_page.html'


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationNewForm(data=request.POST)
        if form.is_valid():
            remember_me = form.cleaned_data.get('remember_me')
            if remember_me:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                request.session.set_expiry(0)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationNewForm()
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile()
            user_profile.user = user
            user_profile.user_type = form.cleaned_data['user_type']
            user_profile.save()

            return render(request, 'registration/account_created.html')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def toggle_favorite(request, pk):
    user = request.user
    apartment = get_object_or_404(Apartment, id=pk)
    favorite = Favorite.objects.filter(user=user, apartment=apartment).first()
    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(user=user, apartment=apartment)
    return redirect(request.META.get('HTTP_REFERER'))


class UserProfileUpdateView(UpdateView, LoginRequiredMixin):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)


class ApartmentCreateView(CreateView):
    model = Apartment
    form_class = ApartmentForm
    template_name = 'post_a_room.html'
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('images')
        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.author = request.user
            apartment.save()
            for f in files:
                image_instance = ApartmentImage.objects.create(image=f)
                apartment.images.add(image_instance)
                apartment.save()
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


def browse_rooms(request):
    apartments = Apartment.objects.all().order_by('-date_posted')
    context = {'apartments': apartments}
    return render(request, 'browse_rooms.html', context)


class ApartmentDetailView(DetailView):
    model = Apartment
    template_name = 'apartment_detail.html'
    context_object_name = 'apartment'


class UserProfileView(DetailView):
    model = UserProfile
    template_name = 'user_profile.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
