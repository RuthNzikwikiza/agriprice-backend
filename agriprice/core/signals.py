from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PricePrediction, Notification, Product, UserProfile

# -------------------------------
# Notify when a new PricePrediction is added
# -------------------------------
@receiver(post_save, sender=PricePrediction)
def notify_price_prediction(sender, instance, created, **kwargs):
    if created:
        # Get all users except the one who created the prediction
        recipients = UserProfile.objects.exclude(id=instance.predicted_by.id if instance.predicted_by else None)

        notifications = [
            Notification(
                recipient=recipient,
                product=instance.product,
                price_prediction=instance,
                message=f"New price prediction for {instance.product.name}: {instance.predicted_price}",
                type='price_adjustment',
                is_read=False  # default unread
            )
            for recipient in recipients
        ]
        Notification.objects.bulk_create(notifications)

# -------------------------------
# Notify when a new Product is added
# -------------------------------
@receiver(post_save, sender=Product)
def notify_new_product(sender, instance, created, **kwargs):
    if created:
        recipients = UserProfile.objects.all()

        notifications = [
            Notification(
                recipient=recipient,
                product=instance,
                message=f"New product added: {instance.name}",
                type="new_product",
                is_read=False
            )
            for recipient in recipients
        ]
        Notification.objects.bulk_create(notifications)
