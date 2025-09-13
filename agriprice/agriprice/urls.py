from django.contrib import admin
from django.urls import path, include
from core import views
urlpatterns = [
    path('',views.home),
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
]
