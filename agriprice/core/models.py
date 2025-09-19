# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# users

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)  
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# user profile
ROLE_CHOICES = [
    ('farmer', 'Farmer'),
    ('buyer', 'Buyer'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('verified', 'Verified'),
    ('suspended', 'Suspended'),
]


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='profile')
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    location = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    points = models.PositiveIntegerField(default=0)
    ratings = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.ratings >= 50:
            self.verified = True
            self.status = 'verified'
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.user.username} Profile"


# product
UNIT_CHOICES = [
    ('kg', 'Kilogram'),
    ('ton', 'Ton'),
]

SEASON_CHOICES = [
    ('rainy', 'Rainy'),
    ('dry', 'Dry'),
    ('all', 'All-season'),
]


NOTIFICATION_TYPES = [
    ('price_adjustment', 'Price Adjustment'),
    ('new_product', 'New Product Added'),
]


class PricePrediction(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='price_predictions')
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2)
    predicted_by = models.ForeignKey('UserProfile', on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField(blank=True, null=True)
    season = models.CharField(max_length=16, choices=SEASON_CHOICES, default='all')
    predicted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-predicted_at']
        unique_together = ()  # Temporarily empty; add real fields later

    def __str__(self):
        return f"{self.product.name} ({self.season}): Predicted {self.predicted_price}"


class Notification(models.Model):
    recipient = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='notifications')
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    price_prediction = models.ForeignKey('PricePrediction', on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        recipient_name = getattr(self.recipient, 'user', 'Unknown')
        return f"Notification for {recipient_name} - {self.message[:20]}"


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
