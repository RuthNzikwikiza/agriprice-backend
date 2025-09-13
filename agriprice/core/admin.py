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


