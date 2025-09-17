from rest_framework import serializers
from .models import ROLE_CHOICES, User, UserProfile, Product, PricePrediction, Notification

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, role=role, phone_number="", location="")
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['owner', 'created_at'] 
class PricePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePrediction
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
