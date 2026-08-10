from django.db import models
from django.conf import settings

class SavedItinerary(models.Model):
    BUDGET_CHOICES = [
        ('budget', 'Budget-friendly'),
        ('mid_range', 'Mid-range'),
        ('luxury', 'Luxury / High-end'),
    ]
    
    STYLE_CHOICES = [
        ('adventure', 'Adventure & Exploration'),
        ('relaxed', 'Relaxed & Leisurely'),
        ('cultural', 'Cultural & Historical'),
        ('foodie', 'Culinary & Foodie tour'),
        ('general', 'General Sightseeing'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='itineraries')
    destination = models.CharField(max_length=150)
    duration_days = models.PositiveIntegerField(default=3)
    budget_category = models.CharField(max_length=20, choices=BUDGET_CHOICES, default='mid_range')
    travel_style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='general')
    interests = models.TextField(blank=True, null=True)
    
    # AI generated content fields
    itinerary_content = models.TextField()
    budget_estimate = models.TextField(blank=True, null=True)
    packing_list = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.duration_days}-Day Itinerary for {self.destination} ({self.user.username})"

class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats')
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Chat by {self.user.username} at {self.created_at}"
