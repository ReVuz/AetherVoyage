from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('checkout/<int:package_id>/', views.booking_checkout, name='booking_checkout'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
]
