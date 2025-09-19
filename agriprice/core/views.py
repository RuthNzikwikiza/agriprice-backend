# core/views.py
from rest_framework import generics
from .models import PricePrediction, Notification
from .serializers import PricePredictionSerializer, NotificationSerializer

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


