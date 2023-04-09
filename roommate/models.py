from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def get_upload_path(object_, filename):
    if isinstance(object_, UserProfile):
        return f'{object_.user.username}/avatars/{filename}'
    elif isinstance(object_, ApartmentImage):
        return f'{object_.apartment.author.username}/apartment_pics/{filename}'
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
    images = models.ManyToManyField('ApartmentImage', blank=True, related_name='apartments')

    def __str__(self):
        return f'{self.author.first_name} {self.address} {self.city} {self.state}'

    def is_favorite(self):
        return Favorite.objects.filter(apartment=self).first() is not None


class ApartmentImage(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=get_upload_path, null=True, blank=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'apartment')


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    USER_TYPE_CHOICES = [
        ('provider', 'Roommate Provider'),
        ('seeker', 'Roommate Seeker'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
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

    def is_profile_complete(self):
        required_fields = ['first_name', 'last_name', 'gender', 'birthdate']
        return all(getattr(self, field) for field in required_fields)

    def is_all_data_complete(self):
        return self.is_profile_complete() and self.user.preference.is_complete() and self.user.lifestyle.is_complete()


class UserPreference(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('any', 'Any')
    ]

    SMOKING_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('indifferent', 'Indifferent'),
    ]

    PETS_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('indifferent', 'Indifferent'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')
    preferred_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='any')
    preferred_age_min = models.PositiveIntegerField(default=18)
    preferred_age_max = models.PositiveIntegerField(default=100)
    smoking_preference = models.CharField(max_length=12, choices=SMOKING_CHOICES, default='indifferent')
    pets_preference = models.CharField(max_length=12, choices=PETS_CHOICES, default='indifferent')

    def is_complete(self):
        # Add the required fields for UserPreference here.
        required_fields = ['preferred_gender', 'preferred_age_min', 'preferred_age_max']
        return all(getattr(self, field) for field in required_fields)


class Lifestyle(models.Model):
    # Sample fields for the Lifestyle model
    WORK_SCHEDULE_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('night', 'Night'),
        ('flexible', 'Flexible'),
    ]

    CLEANLINESS_CHOICES = [
        ('very_clean', 'Very Clean'),
        ('clean', 'Clean'),
        ('moderate', 'Moderate'),
        ('messy', 'Messy'),
    ]

    SOCIAL_CHOICES = [
        ('very_social', 'Very Social'),
        ('social', 'Social'),
        ('moderate', 'Moderate'),
        ('not_social', 'Not Social'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lifestyle')
    work_schedule = models.CharField(max_length=10, choices=WORK_SCHEDULE_CHOICES, default='flexible')
    cleanliness = models.CharField(max_length=10, choices=CLEANLINESS_CHOICES, default='moderate')
    social = models.CharField(max_length=11, choices=SOCIAL_CHOICES, default='moderate')
    interests = models.TextField(blank=True)
    hobbies = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} - Lifestyle'

    def is_complete(self):
        # Add the required fields for Lifestyle here.
        required_fields = ['work_schedule', 'cleanliness', 'social', 'interests', 'hobbies']
        return all(getattr(self, field) for field in required_fields)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username} - {self.timestamp}'
