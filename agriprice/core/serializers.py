from rest_framework import serializers
from .models import ROLE_CHOICES, User, UserProfile, Product, PricePrediction, Notification
from cloudinary_storage.storage import MediaCloudinaryStorage

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
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', required=True)
    profile_photo = serializers.ImageField(required=False, allow_null=True, use_url=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'email', 'role', 'profile_photo', 'phone_number',
            'location', 'verified', 'points', 'ratings', 'status', 'bio'
        ]
        read_only_fields = ['points', 'ratings', 'status', 'verified']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        email = user_data.get('email')
        if email and instance.user.email != email:
            instance.user.email = email
            instance.user.save()
        profile_photo = validated_data.get('profile_photo', None)
        if profile_photo:
            instance.profile_photo = profile_photo

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    owner_username = serializers.SerializerMethodField()  
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'unit', 'season',
            'image', 'image_url', 'owner_username', 'created_at'
        ]
        read_only_fields = ['owner', 'created_at']

    def get_owner_username(self, obj):
        if obj.owner and hasattr(obj.owner, 'user'):
            return obj.owner.user.username
        return "Unknown"

    def get_image_url(self, obj):
        if obj.image:
            try:
                return obj.image.url
            except Exception as e:
                print(f"Error getting image URL: {e}")
                return None
        return None
class PricePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePrediction
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
