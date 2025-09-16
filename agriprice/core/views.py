from rest_framework import generics, viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import UserProfile, Product
from .serializers import UserSerializer, UserProfileSerializer, ProductSerializer
from .permissions import IsFarmerOrReadOnly, IsBuyer
from .models import  UserProfile, Product
from .serializers import UserProfileSerializer, ProductSerializer
from rest_framework.views import APIView
from .models import PricePrediction, Notification 
from .serializers import PricePredictionSerializer, NotificationSerializer
from rest_framework import permissions
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello Agriprice is live")
# Registration
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        user = serializer.save()
        return Response({
            "message": "User created successfully",
            "username": user.username,
            "email": user.email,
            "role": user.profile.role
        }, status=status.HTTP_201_CREATED)
# Price Predictions Views

class PricePredictionListCreateView(generics.ListCreateAPIView):
    queryset = PricePrediction.objects.all()
    serializer_class = PricePredictionSerializer
    permission_classes = [permissions.IsAuthenticated]

# JWT login with email
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'


    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(request=self.context.get('request'), email=email, password=password)
        # user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")
            return super().validate(attrs)
class PricePredictionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PricePrediction.objects.all()
    serializer_class = PricePredictionSerializer
    permission_classes = [permissions.IsAuthenticated]



class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

# UserProfile viewset
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsBuyer]

# Product viewset
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsFarmerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'season']

# Notifications Views
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter().order_by('-created_at')


# Retrieve a single notification (optional)
class NotificationDetailView(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user.userprofile)


# Mark a notification as read
class NotificationMarkReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user.userprofile)
            notification.is_read = True
            notification.save()
            return Response({"detail": "Notification marked as read"}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"detail": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

