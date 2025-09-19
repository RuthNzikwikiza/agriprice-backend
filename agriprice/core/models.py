# core/models.py
from django.db import models

# ----------------------
# TEMP STUBS (remove later)
# ----------------------


class UserProfile(models.Model):
    user = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)

# real models


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
