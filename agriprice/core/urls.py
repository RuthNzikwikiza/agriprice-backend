from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, ProductViewSet, RegisterView, EmailTokenObtainPairView, TokenRefreshView, PricePredictionListCreateView, PricePredictionRetrieveUpdateDeleteView, NotificationListView

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('price-predictions/', PricePredictionListCreateView.as_view(), name='price-predictions-list-create'),
    path('price-predictions/<int:pk>/', PricePredictionRetrieveUpdateDeleteView.as_view(), name='price-predictions-rud'),
    path('notifications/', NotificationListView.as_view(), name='notifications-list'),
]
