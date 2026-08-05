from django import forms
from .models import Destination, TourPackage, Review

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'location', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Kyoto'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Japan'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = [
            'destination', 'title', 'description', 'price', 
            'duration_days', 'start_date', 'end_date', 'max_slots', 
            'available_slots', 'image', 'is_active'
        ]
        widgets = {
            'destination': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Historic Kyoto Cultural Tour'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'max_slots': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'available_slots': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        max_slots = cleaned_data.get('max_slots')
        available_slots = cleaned_data.get('available_slots')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("Start date must be before the end date.")

        if max_slots and available_slots and available_slots > max_slots:
            raise forms.ValidationError("Available slots cannot exceed maximum slots.")
            
        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(5, 0, -1)], attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your experience...'}),
        }
