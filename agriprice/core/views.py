from rest_framework import generics, status, serializers, permissions, viewsets, filters
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UserProfile, Product, PricePrediction, Notification
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    ProductSerializer,
    PricePredictionSerializer,
    NotificationSerializer,
)
from .permissions import IsFarmerOrReadOnly, IsBuyer
from rest_framework.permissions import IsAuthenticated

def home(request):
    return HttpResponse("Hello Agriprice is live")

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, "profile", None)
        if not profile:
            return Response({"detail": "Profile not created yet"}, status=status.HTTP_200_OK)

        return Response({
            "username": user.username,
            "email": user.email,
            "role": profile.role,
            "phone_number": profile.phone_number,
            "location": profile.location,
            "verified": profile.verified,
            "points": profile.points,
            "ratings": str(profile.ratings),
            "status": profile.status,
            "bio": profile.bio,
            "profile_photo": request.build_absolute_uri(profile.profile_photo.url) if profile.profile_photo else None
        })
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        profile = getattr(request.user, 'profile', None)
        if not profile:
            return Response({"detail": "Profile not created yet"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = getattr(request.user, 'profile', None)
        if not profile:
            serializer = UserProfileSerializer(data=request.data)
        else:
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated, IsFarmerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'season']
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)
    def update(self, request, *args, **kwargs):
        product = self.get_object()
        if product.owner != request.user.profile:
            raise PermissionDenied("You cannot edit someone else's product")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.owner != request.user.profile:
            raise PermissionDenied("You cannot delete someone else's product")
        return super().destroy(request, *args, **kwargs)
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
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
