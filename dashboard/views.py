from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Sum
from accounts.decorators import admin_required, staff_required, customer_required

from bookings.models import Booking
from packages.models import TourPackage, Destination
from ai_itinerary.models import SavedItinerary

User = get_user_model()

@login_required
def redirect_dashboard(request):
    """
    Redirects user to the correct dashboard based on their role.
    """
    if request.user.role == 'admin' or request.user.is_superuser:
        return redirect('dashboard:admin_dashboard')
    elif request.user.role == 'staff' or request.user.is_staff:
        return redirect('dashboard:staff_dashboard')
    else:
        return redirect('dashboard:customer_dashboard')

@login_required
@customer_required
def customer_dashboard(request):
    """
    Retrieve customer-specific bookings, saved itineraries, and spending history.
    """
    bookings = Booking.objects.filter(user=request.user).select_related('package', 'package__destination')
    itineraries = SavedItinerary.objects.filter(user=request.user)
    
    # Calculate approved spendings
    approved_spent = bookings.filter(status='approved').aggregate(Sum('total_price'))['total_price__sum'] or 0.0
    
    context = {
        'bookings': bookings,
        'itineraries': itineraries,
        'stats': {
            'total_bookings': bookings.count(),
            'total_spent': approved_spent,
            'total_itineraries': itineraries.count(),
        }
    }
    return render(request, 'dashboard/customer_dashboard.html', context)

@login_required
@staff_required
def staff_dashboard(request):
    """
    Retrieve staff dashboard showing pending reservations, total inventory counts, and status filters.
    """
    pending_bookings = Booking.objects.filter(status='pending').select_related('user', 'package', 'package__destination')
    active_packages = TourPackage.objects.filter(is_active=True).select_related('destination')[:5]
    
    context = {
        'pending_bookings': pending_bookings,
        'active_packages': active_packages,
        'stats': {
            'pending_count': Booking.objects.filter(status='pending').count(),
            'packages_count': TourPackage.objects.count(),
            'destinations_count': Destination.objects.count(),
        }
    }
    return render(request, 'dashboard/staff_dashboard.html', context)

@login_required
@admin_required
def admin_dashboard(request):
    """
    Retrieve global system stats (users count, bookings, gross approved revenue).
    """
    recent_bookings = Booking.objects.all().select_related('user', 'package', 'package__destination')[:10]
    total_revenue = Booking.objects.filter(status='approved').aggregate(Sum('total_price'))['total_price__sum'] or 0.0
    
    context = {
        'recent_bookings': recent_bookings,
        'stats': {
            'total_users': User.objects.count(),
            'total_bookings': Booking.objects.count(),
            'total_revenue': total_revenue,
            'packages_count': TourPackage.objects.count(),
        }
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
