from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import EmailInput, Textarea, DateInput, TextInput, URLInput

from roommate.models import UserProfile, Apartment


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'email': EmailInput(attrs={'placeholder': 'Please enter your email'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_pic', 'first_name', 'last_name', 'bio', 'birthdate', 'location', 'phone_number',
                  'social_facebook', 'social_twitter', 'social_instagram')
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control-file', 'placeholder': 'Choose a file...'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name...'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name...'}),
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
