from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, ProductViewSet, RegisterView,EmailTokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    # Price Predictions
    path('price-predictions/', views.PricePredictionListCreateView.as_view(),
         name='price-predictions-list-create'),
    path('price-predictions/<int:pk>/', views.PricePredictionRetrieveUpdateDeleteView.as_view(),
         name='price-predictions-rud'),

    # Notifications
    path('notifications/', views.NotificationListCreateView.as_view(),
         name='notifications-list-create'),
    path('notifications/<int:pk>/', views.NotificationRetrieveUpdateDeleteView.as_view(),
         name='notifications-rud'),

    # Router endpoints (profiles, products)
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('auth/login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
