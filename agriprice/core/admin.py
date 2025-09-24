from django.contrib import admin
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
