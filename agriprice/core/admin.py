from django.contrib import admin
from .models import PricePrediction, Notification


class PricePredictionAdmin(admin.ModelAdmin):
    list_display = ('predicted_price', 'season', 'predicted_at') 
    list_filter = ('season', 'predicted_at')
    search_fields = ('reason',)
    ordering = ('-predicted_at',)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'type', 'is_read', 'created_at')
    list_filter = ('type', 'is_read', 'created_at')
    search_fields = ('message',)
    ordering = ('-created_at',)


admin.site.register(PricePrediction, PricePredictionAdmin)
admin.site.register(Notification, NotificationAdmin)
