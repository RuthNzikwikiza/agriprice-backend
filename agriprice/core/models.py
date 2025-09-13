# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# users
class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "This email is already registered. Please use another one.",
        }
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            'unique': "This username is already taken. Please choose another one.",
        }
    )

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return self.username


# User Profile
ROLE_CHOICES = [
    ('farmer', 'Farmer'),
    ('buyer', 'Buyer'),
]

STATUS_CHOICES = [
    ('active', 'Active'),
    ('suspended', 'Suspended'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    location = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    points = models.PositiveIntegerField(default=0)
    ratings = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.ratings >= 50:
            self.verified = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} Profile"


# Product
UNIT_CHOICES = [
    ('kg', 'Kilogram'),
    ('ton', 'Ton'),
]

SEASON_CHOICES = [
    ('rainy', 'Rainy'),
    ('dry', 'Dry'),
    ('all', 'All-season'),
]


class Product(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    season = models.CharField(max_length=16, choices=SEASON_CHOICES, default='all')

    class Meta:
        unique_together = ('owner', 'name')

    def __str__(self):
        return f"{self.name} - {self.price}"
