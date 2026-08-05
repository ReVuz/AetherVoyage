"""
URL configuration for AetherVoyage project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('dashboard:redirect_dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('packages/', include('packages.urls', namespace='packages')),
    path('bookings/', include('bookings.urls', namespace='bookings')),
    path('ai/', include('ai_itinerary.urls', namespace='ai_itinerary')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
