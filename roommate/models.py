from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    price = models.DecimalField(max_digits=8, decimal_places=2)
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

    def __str__(self):
        return f'{self.author.first_name} {self.address} {self.city} {self.state}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='static/avatars/', blank=True)
    bio = models.CharField(max_length=500, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    social_facebook = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True)
    social_instagram = models.URLField(blank=True)
    messages = models.ManyToManyField(Message, blank=True)
    received_messages = models.ManyToManyField(Message, related_name='receiver')
    sent_messages = models.ManyToManyField(Message, related_name='sender')

    def __str__(self):
        return self.user.username

    def get_received_messages(self):
        return self.received_messages.all()

    def get_sent_messages(self):
        return self.sent_messages.all()


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'room']


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



