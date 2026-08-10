from django.contrib import admin
from .models import SavedItinerary, ChatHistory

@admin.register(SavedItinerary)
class SavedItineraryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'destination', 'duration_days', 'budget_category', 'travel_style', 'created_at']
    list_filter = ['budget_category', 'travel_style', 'created_at']
    search_fields = ['destination', 'user__username']

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    search_fields = ['user__username', 'message', 'response']
