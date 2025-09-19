
# core/views.py
from rest_framework import generics
from .models import PricePrediction, Notification, UserProfile, Product
from .serializers import PricePredictionSerializer, NotificationSerializer, UserProfileSerializer, ProductSerializer
from rest_framework import viewsets


# prediction price
class PricePredictionListCreateView(generics.ListCreateAPIView):
    queryset = PricePrediction.objects.all()
    serializer_class = PricePredictionSerializer


class PricePredictionRetrieveUpdateDeleteView(generics.
                                              RetrieveUpdateDestroyAPIView):
    queryset = PricePrediction.objects.all()
    serializer_class = PricePredictionSerializer

# notifications


class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationRetrieveUpdateDeleteView(generics.
                                           RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

