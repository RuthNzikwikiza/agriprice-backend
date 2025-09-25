from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import (
    CurrentUserView,
    UserProfileViewSet,
    ProductViewSet,
    RegisterView,
    EmailTokenObtainPairView,
    TokenRefreshView,
    PricePredictionListCreateView,
    PricePredictionRetrieveUpdateDeleteView,
    NotificationListView,
    NotificationDetailView,
    NotificationMarkReadView,
    UpdateProfileView,  
    home,
)

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('', include(router.urls)),

    # Current user profile
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    path('users/me/edit/', UpdateProfileView.as_view(), name='update-profile'),  

    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Price predictions
    path('price-predictions/', PricePredictionListCreateView.as_view(), name='price-predictions-list-create'),
    path('price-predictions/<int:pk>/', PricePredictionRetrieveUpdateDeleteView.as_view(), name='price-predictions-rud'),

    # Notifications
    path('notifications/', NotificationListView.as_view(), name='notifications-list'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('notifications/<int:pk>/read/', NotificationMarkReadView.as_view(), name='notification-mark-read'),
]
