from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


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
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    location = models.CharField(max_length=100, blank=True)
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
        unique_together = ('product', 'season', 'predicted_by')  

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

