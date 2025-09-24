from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import PricePrediction, Notification, Product, UserProfile


# automatic notifications for for PricePrediction

@receiver(post_save, sender=PricePrediction)
def notify_price_prediction(sender, instance, created, **kwargs):
    if created:
     
        if hasattr(instance.product, 'users'):
            recipients = instance.product.users.all()  
        else:
            recipients = UserProfile.objects.all()  

        notifications = [
            Notification(
                recipient=recipient,
                product=instance.product,
                price_prediction=instance,
                message=f"New price prediction for {instance.product.name}: {instance.predicted_price}",
                type='price_adjustment'
            )
            for recipient in recipients
        ]
        Notification.objects.bulk_create(notifications)


# automatic notifications for new Product

@receiver(post_save, sender=Product)
def notify_new_product(sender, instance, created, **kwargs):
    if created:
        recipients = UserProfile.objects.all()  

        notifications = [
            Notification(
                recipient=recipient,
                product=instance,
                message=f"New product added: {instance.name}",
                type="new_product"
            )
            for recipient in recipients
        ]
        Notification.objects.bulk_create(notifications)
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        UserProfile.objects.create(
            user=instance,
            role=getattr(instance, 'role', 'buyer') 
        )