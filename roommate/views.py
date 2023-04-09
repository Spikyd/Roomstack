from datetime import date
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q, Subquery, OuterRef
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView, CreateView, DetailView, FormView, ListView

from roommate.filters import ApartmentFilter
from roommate.forms import UserRegisterForm, UserProfileForm, ApartmentForm, AuthenticationNewForm, UserPreferenceForm, \
    LifestyleForm, MessageForm
from roommate.models import Apartment, UserProfile, Favorite, ApartmentImage, UserPreference, Lifestyle, Message


class HomeTemplateView(TemplateView):
    template_name = 'home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add an apartment variable to the context dictionary
        apartment = Apartment.objects.first()
        context['apartment'] = apartment
        return context


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
            user_profile.gender = form.cleaned_data['gender']  # Save the gender to UserProfile
            user_profile.save()
            UserPreference.objects.create(user=user)
            Lifestyle.objects.create(user=user)
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


class UserProfileUpdateView(LoginRequiredMixin, FormView):
    template_name = 'settings.html'

    def get(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        profile_form = UserProfileForm(instance=user_profile)
        preference_form = UserPreferenceForm(instance=request.user.preference)  # Use UserPreference instance
        lifestyle_form = LifestyleForm(instance=request.user.lifestyle)
        return render(request, self.template_name, {'profile_form': profile_form, 'preference_form': preference_form,
                                                    'lifestyle_form': lifestyle_form})

    def post(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        form_type = request.POST.get('form_type')
        if form_type == 'profile_form':
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        elif form_type == 'preference_form':
            form = UserPreferenceForm(request.POST, instance=request.user.preference)  # Use UserPreference instance
        elif form_type == 'lifestyle_form':
            form = LifestyleForm(request.POST, instance=request.user.lifestyle)
        else:
            return HttpResponseBadRequest('Invalid form type')

        if form.is_valid():
            form.save()
            messages.success(request, 'Changes saved successfully.')
            return redirect('home')

        profile_form = UserProfileForm(instance=user_profile)
        preference_form = UserPreferenceForm(instance=request.user.preference)  # Use UserPreference instance
        lifestyle_form = LifestyleForm(instance=request.user.lifestyle)
        return render(request, self.template_name, {'profile_form': profile_form, 'preference_form': preference_form,
                                                    'lifestyle_form': lifestyle_form})


class ApartmentCreateView(LoginRequiredMixin, CreateView):
    model = Apartment
    form_class = ApartmentForm
    template_name = 'post_a_room.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.user_type == 'seeker':
            messages.error(request, 'You are not allowed to post a room.')
            return redirect('home')
        elif Apartment.objects.filter(author=user).exists():
            messages.error(request, 'You are not allowed to post more than one room.')
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('images')
        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.author = request.user
            apartment.save()
            for f in files:
                image_instance = ApartmentImage.objects.create(image=f, apartment=apartment)
                apartment.images.add(image_instance)
                apartment.save()
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


@login_required
def browse_rooms(request):
    apartment_list = Apartment.objects.all().order_by('-date_posted')
    filter = ApartmentFilter(request.GET, queryset=apartment_list)
    filtered_apartments = filter.qs
    context = {
        'apartments': apartment_list,
        'filtered_apartments': filtered_apartments,
        'filter': filter,
    }
    # Add an apartment variable to the context dictionary
    apartment = apartment_list.first()
    context['apartment'] = apartment
    return render(request, 'browse_rooms.html', context)


class ApartmentDetailView(LoginRequiredMixin, DetailView):
    model = Apartment
    template_name = 'apartment_detail.html'
    context_object_name = 'apartment'


class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'user_profile.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        user_pk = self.kwargs.get('pk')
        return get_object_or_404(UserProfile, user__pk=user_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ApartmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Apartment
    form_class = ApartmentForm
    template_name = 'manage_apartment.html'

    def test_func(self):
        apartment = self.get_object()
        return self.request.user == apartment.author

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to edit this apartment.")
        return redirect('browse_rooms')

    def get_success_url(self):
        return reverse_lazy('apartment_detail', args=[self.object.pk])


@login_required
def delete_apartment(request, pk):
    Apartment.objects.filter(id=pk).delete()
    return redirect('browse_rooms')


@login_required
def favorite_rooms(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorite_rooms.html', {'favorites': favorites})


class MatchFinder(LoginRequiredMixin, View):

    @staticmethod
    def calculate_compatibility(user, other_user, user_preference, other_user_preference):
        if user.userprofile.birthdate is None or other_user.userprofile.birthdate is None:
            return 0  # If either user's birthdate is not set, skip this user and return a compatibility percentage of 0

        user_age = (date.today() - user.userprofile.birthdate).days // 365
        other_user_age = (date.today() - other_user.userprofile.birthdate).days // 365

        fixed_score_categories = 7
        score = 0

        # Check for gender preference match
        if user_preference.preferred_gender in (
                other_user.userprofile.gender, 'any') and other_user_preference.preferred_gender in (
                user.userprofile.gender, 'any'):
            score += 1

        # Check for age preference match
        age_match = user_preference.preferred_age_min <= other_user_age <= user_preference.preferred_age_max
        other_age_match = other_user_preference.preferred_age_min <= user_age <= other_user_preference.preferred_age_max
        if age_match and other_age_match:
            score += 1

        # Check for smoking preference match
        if other_user.preference.smoking_preference in (
                user_preference.smoking_preference, 'indifferent') and user.preference.smoking_preference in (
                other_user_preference.smoking_preference, 'indifferent'):
            score += 1

        # Check for pets preference match
        if other_user.preference.pets_preference in (
                user_preference.pets_preference, 'indifferent') and user.preference.pets_preference in (
                other_user_preference.pets_preference, 'indifferent'):
            score += 1

        # Check for work schedule match
        if user.lifestyle.work_schedule == other_user.lifestyle.work_schedule:
            score += 1

        # Check for cleanliness match
        if user.lifestyle.cleanliness == other_user.lifestyle.cleanliness:
            score += 1

        # Check for social match
        if user.lifestyle.social == other_user.lifestyle.social:
            score += 1

        # Calculate common interests and hobbies
        common_interests = set(user.lifestyle.interests.split(', ')) & set(
            other_user.lifestyle.interests.split(', '))
        common_hobbies = set(user.lifestyle.hobbies.split(', ')) & set(
            other_user.lifestyle.hobbies.split(', '))

        # Add common interests and hobbies count to the score
        score += len(common_interests) + len(common_hobbies)

        # Calculate max_score dynamically
        max_interests = max(len(user.lifestyle.interests.split(', ')), len(other_user.lifestyle.interests.split(', ')))
        max_hobbies = max(len(user.lifestyle.hobbies.split(', ')), len(other_user.lifestyle.hobbies.split(', ')))
        max_score = fixed_score_categories + max_interests + max_hobbies

        compatibility_percentage = (score / max_score) * 100

        return compatibility_percentage

    def get(self, request, *args, **kwargs):
        user = request.user
        user_preference = user.preference

        # Check if the user is a provider
        if user.userprofile.user_type != 'seeker':
            messages.error(request, "Access restricted. This page is available only for seeker users.")
            return redirect('home')  # Redirect to a different page, e.g., home or user profile

        # Filter users who have a profile and are providers
        users = User.objects.exclude(id=user.id).exclude(userprofile=None).filter(userprofile__user_type='provider',
                                                                                  apartment__isnull=False)

        scored_users = []
        for other_user in users:
            other_user_preference = other_user.preference  # Get the other user's preferences
            compatibility = self.calculate_compatibility(user, other_user, user_preference, other_user_preference)
            scored_users.append((other_user, compatibility))

        scored_users.sort(key=lambda x: x[1], reverse=True)

        context = {
            'matched_users': scored_users,
            'current_user': request.user,
        }
        return render(request, 'matched_users.html', context)


@login_required
def messages_view(request, user_id):
    user = User.objects.get(pk=user_id)
    # Fetch users with conversations
    users_with_conversations = User.objects.filter(
        Q(sent_messages__receiver=request.user) | Q(received_messages__sender=request.user)
    ).distinct()

    # Calculate compatibility score using the same preference settings for both users
    compatibility_score = MatchFinder.calculate_compatibility(request.user, user, request.user.preference,
                                                              user.preference)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = user
            message.save()
            return redirect('messages_view', user_id=user_id)
    else:
        form = MessageForm()

    messages = Message.objects.filter(sender=request.user, receiver=user) | Message.objects.filter(sender=user,
                                                                                                   receiver=request.user)
    messages = messages.order_by('timestamp')

    # Mark messages as read
    unread_messages = messages.filter(receiver=request.user, is_read=False)
    unread_messages.update(is_read=True)

    return render(request, 'messages.html',
                  {'form': form, 'chat_messages': messages, 'receiver': user,
                   'users_with_conversations': users_with_conversations, 'suppress_messages_modal': True,
                   'compatibility_score': compatibility_score, })


class UnreadMessagesView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'unread_messages.html'
    context_object_name = 'conversations'

    def get_queryset(self):
        latest_messages = Message.objects.filter(receiver=self.request.user, is_read=False,
                                                 sender=OuterRef('sender')).order_by('-timestamp')
        return Message.objects.filter(receiver=self.request.user, is_read=False,
                                      timestamp=Subquery(latest_messages.values('timestamp')[:1])).order_by(
            '-timestamp')


@login_required
def conversations_view(request):
    # Fetch users with conversations
    users_with_conversations = User.objects.filter(
        Q(sent_messages__receiver=request.user) | Q(received_messages__sender=request.user)
    ).distinct()

    return render(request, 'conversations.html', {'users_with_conversations': users_with_conversations})
