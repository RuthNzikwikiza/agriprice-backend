from rest_framework import generics, status, serializers, permissions, viewsets, filters
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.http import HttpResponse

from .models import UserProfile, Product, PricePrediction, Notification
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    ProductSerializer,
    PricePredictionSerializer,
    NotificationSerializer,
)
from .permissions import IsFarmerOrReadOnly, IsBuyer


def home(request):
    return HttpResponse("Hello Agriprice is live")


# ----------------------------
# Registration
# ----------------------------
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        profile = getattr(user, "profile", None)
        return Response({
            "message": "User created successfully",
            "username": user.username,
            "email": user.email,
            "role": profile.role if profile else None
        }, status=status.HTTP_201_CREATED)


# ----------------------------
# JWT Login with email
# ----------------------------
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password
        )
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        data = super().validate(attrs)
        data["email"] = user.email
        data["username"] = user.username
        data["role"] = getattr(user.profile, "role", None)
        return data


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


# ----------------------------
# Price Predictions
# ----------------------------
class PricePredictionListCreateView(generics.ListCreateAPIView):
    queryset = PricePrediction.objects.all()
    serializer_class = PricePredictionSerializer
    permission_classes = [permissions.IsAuthenticated]


class PricePredictionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PricePrediction.objects.all()
    serializer_class = PricePredictionSerializer
    permission_classes = [permissions.IsAuthenticated]


# ----------------------------
# UserProfile
# ----------------------------
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsBuyer]


# ----------------------------
# Product
# ----------------------------
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsFarmerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'season']
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile,)
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user.profile).order_by('-created_at')


class NotificationDetailView(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user.profile)


class NotificationMarkReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user.profile)
            notification.is_read = True
            notification.save()
            return Response({"detail": "Notification marked as read"}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"detail": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
