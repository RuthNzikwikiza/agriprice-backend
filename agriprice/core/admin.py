from django.contrib import admin
from .models import PricePrediction, Notification
from django.contrib.auth.admin import UserAdmin 
from .models import User, UserProfile, Product


class PricePredictionAdmin(admin.ModelAdmin):
    list_display = ('predicted_price', 'product', 'created_at') 
    list_filter = ('product', 'created_at')
    search_fields = ('reason',)
    ordering = ('-created_at',)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'read', 'created_at')
    list_filter = ('user', 'read', 'created_at')
    search_fields = ('message',)
    ordering = ('-created_at',)


admin.site.register(PricePrediction, PricePredictionAdmin)
admin.site.register(Notification, NotificationAdmin)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'verified', 'points', 'status')
    search_fields = ('user__username', 'user__email', 'phone_number')
    list_filter = ('role', 'verified', 'status')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'price', 'unit')  
    search_fields = ('name', 'owner__user__username')  
    list_filter = ('unit', 'season')  


