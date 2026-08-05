from django.contrib import admin
from .models import Destination, TourPackage, Review

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'created_at']
    search_fields = ['name', 'location']

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'destination', 'price', 'duration_days', 'available_slots', 'is_active']
    list_filter = ['is_active', 'destination']
    search_fields = ['title', 'description']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['package', 'user', 'rating', 'created_at']
    list_filter = ['rating']
