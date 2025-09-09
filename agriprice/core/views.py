from django.shortcuts import render
from rest_framework import viewsets
from .models import UserProfile, Product
from .serializers import UserProfileSerializer, ProductSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
