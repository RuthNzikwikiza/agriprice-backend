# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Price Predictions
    path('price-predictions/', views.PricePredictionListCreateView.as_view(), name='price-predictions-list-create'),
    path('price-predictions/<int:pk>/', views.PricePredictionRetrieveUpdateDeleteView.as_view(), name='price-predictions-rud'),


    # Notifications (read-only)
    path('notifications/', views.NotificationListView.as_view(), name='notifications-list'),
]
