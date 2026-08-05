from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Destination(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.location}"

class TourPackage(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    duration_days = models.IntegerField(validators=[MinValueValidator(1)])
    start_date = models.DateField()
    end_date = models.DateField()
    max_slots = models.IntegerField(validators=[MinValueValidator(1)])
    available_slots = models.IntegerField()
    image = models.ImageField(upload_to='packages/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.duration_days} Days)"

    def save(self, *args, **kwargs):
        # Initialize available slots if not set yet
        if self.available_slots is None:
            self.available_slots = self.max_slots
        super().save(*args, **kwargs)

class Review(models.Model):
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} for {self.package.title} - Rating: {self.rating}"
