from django.contrib import admin

from django.contrib.auth.admin import UserAdmin 
from .models import User, UserProfile, Product


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



from .models import PricePrediction, Notification


# PricePrediction admin
class PricePredictionAdmin(admin.ModelAdmin):
    list_display = ('predicted_price', 'season', 'predicted_at') 
    list_filter = ('season', 'predicted_at')
    search_fields = ('reason',)
    ordering = ('-predicted_at',)


# Notification admin (read-only)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'type', 'is_read', 'created_at')
    list_filter = ('type', 'is_read', 'created_at')
    search_fields = ('message',)
    ordering = ('-created_at',)
    readonly_fields = ('message', 'type', 'is_read', 'created_at')  # fields cannot be edited
   
    def has_add_permission(self, request):
        return False
  
    def has_delete_permission(self, request, obj=None):
        return False


# Register models
admin.site.register(PricePrediction, PricePredictionAdmin)
admin.site.register(Notification, NotificationAdmin)

