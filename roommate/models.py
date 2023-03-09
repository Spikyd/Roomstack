from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def get_upload_path(object_, filename):
    if isinstance(object_, UserProfile):
        return f'{object_.user.username}/avatars/{filename}'
    elif isinstance(object_, Apartment):
        return f'{object_.author.username}/apartment_pics/{filename}'
    else:
        return f'{filename}'


class Apartment(models.Model):
    BEDROOM_CHOICES = [
        ('Private', 'Private'),
        ('Shared', 'Shared'),
    ]

    BATHROOM_CHOICES = [
        ('Private', 'Private'),
        ('Shared', 'Shared'),
    ]
    # Basic information

    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=8, decimal_places=0)
    bedrooms = models.CharField(max_length=7, choices=BEDROOM_CHOICES, default='Private')
    bathrooms = models.CharField(max_length=7, choices=BATHROOM_CHOICES, default='Private')
    move_in_date = models.DateField(default=timezone.now)
    date_posted = models.DateTimeField(auto_now_add=True)

    # Features
    is_furnished = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_washing_machine = models.BooleanField(default=False)
    has_dryer = models.BooleanField(default=False)
    has_dishwasher = models.BooleanField(default=False)
    has_air_conditioning = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    has_bbq_facilities = models.BooleanField(default=False)

    # Availability
    is_available = models.BooleanField(default=True)
    available_from = models.DateField(default=timezone.now)

    # Author
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Pictures
    images = models.ManyToManyField('ApartmentImage', blank=True)

    def __str__(self):
        return f'{self.author.first_name} {self.address} {self.city} {self.state}'


class ApartmentImage(models.Model):
    image = models.ImageField(upload_to=get_upload_path)

    def is_favorite(self):
        return Favorite.objects.filter(apartment=self).first() is not None


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'apartment')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    profile_pic = models.ImageField(upload_to=get_upload_path, null=True, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    social_facebook = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True)
    social_instagram = models.URLField(blank=True)

    def __str__(self):
        return self.user.username
