from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.forms import EmailInput, Textarea, DateInput, TextInput, URLInput

from roommate.models import UserProfile, Apartment, UserPreference, Lifestyle, Message


class AuthenticationNewForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your username'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your password'})


class PasswordResetNewForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please confirm your password'})


class UserRegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES, label='Roommate Role')
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type', 'gender']

        widgets = {
            'email': EmailInput(attrs={'placeholder': 'Please enter your email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].widget.attrs.update({'placeholder': 'Please enter your username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Please enter your password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Please enter your password again'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists.")
        return email


class PasswordChangeNewForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control',
                                                         'placeholder': 'Please enter your old password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control',
                                                          'placeholder': 'Please enter your new password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control',
                                                          'placeholder': 'Please enter your new password confirmation'})


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_pic', 'first_name', 'last_name', 'gender', 'bio', 'birthdate', 'location', 'phone_number',
                  'social_facebook', 'social_twitter', 'social_instagram')
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control-file', 'placeholder': 'Choose a file...'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name...'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name...'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'bio': Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us about yourself...'}),
            'birthdate': DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'location': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your location...'}),
            'phone_number': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number...'}),
            'social_facebook': URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Facebook URL...'}),
            'social_twitter': URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Twitter URL...'}),
            'social_instagram': URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Instagram URL...'}),
        }


class ApartmentForm(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Apartment
        fields = ('address', 'city', 'state', 'zipcode', 'price', 'bedrooms', 'bathrooms',
                  'move_in_date', 'is_furnished', 'has_parking', 'has_balcony', 'has_pool',
                  'has_gym', 'has_washing_machine', 'has_dryer', 'has_dishwasher',
                  'has_air_conditioning', 'has_wifi', 'has_bbq_facilities', 'available_from', 'images')

        widgets = {
            'address': forms.TextInput(attrs={'placeholder': '1234 Main St'}),
            'city': forms.TextInput(attrs={'placeholder': 'Los Angeles'}),
            'state': forms.TextInput(attrs={'placeholder': 'California'}),
            'zipcode': forms.TextInput(attrs={'placeholder': '90001'}),
            'price': forms.NumberInput(attrs={'placeholder': '1000'}),
            'move_in_date': forms.DateInput(attrs={'type': 'date'}),
            'available_from': forms.DateInput(attrs={'type': 'date'}),
        }


class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['preferred_gender', 'preferred_age_min', 'preferred_age_max', 'smoking_preference', 'pets_preference']

        widgets = {
            'preferred_gender': forms.Select(attrs={'placeholder': 'Select preferred gender'}),
            'preferred_age_min': forms.NumberInput(attrs={'placeholder': 'Enter minimum preferred age'}),
            'preferred_age_max': forms.NumberInput(attrs={'placeholder': 'Enter maximum preferred age'}),
            'smoking_preference': forms.Select(attrs={'placeholder': 'Select smoking preference'}),
            'pets_preference': forms.Select(attrs={'placeholder': 'Select pets preference'}),
        }


class LifestyleForm(forms.ModelForm):

    interests = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter interests separated by commas'}),
        strip=False
    )
    hobbies = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter hobbies separated by commas'}),
        strip=False
    )

    class Meta:
        model = Lifestyle
        fields = ['work_schedule', 'cleanliness', 'social', 'interests', 'hobbies']

    def __init__(self, *args, **kwargs):
        super(LifestyleForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['interests'].initial = self.instance.interests
            self.fields['hobbies'].initial = self.instance.hobbies


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']