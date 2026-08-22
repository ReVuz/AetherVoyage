import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
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
    Retrieve global system stats, monthly booking trends, and popular destinations.
    Passes chart-ready JSON data to the template.
    """
    recent_bookings = Booking.objects.all().select_related('user', 'package', 'package__destination')[:10]
    total_revenue = Booking.objects.filter(status='approved').aggregate(Sum('total_price'))['total_price__sum'] or 0.0

    # --- Chart 1: Monthly Bookings Volume (last 6 months) ---
    monthly_qs = (
        Booking.objects
        .annotate(month=TruncMonth('booking_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    # Keep last 6 data points
    monthly_qs = list(monthly_qs)[-6:]
    monthly_labels = [m['month'].strftime('%b %Y') for m in monthly_qs]
    monthly_data   = [m['count'] for m in monthly_qs]

    # --- Chart 2: Top 5 Popular Destinations by bookings ---
    top_destinations_qs = (
        Booking.objects
        .values('package__destination__name')
        .annotate(booking_count=Count('id'))
        .order_by('-booking_count')[:5]
    )
    dest_labels = [d['package__destination__name'] or 'Unknown' for d in top_destinations_qs]
    dest_data   = [d['booking_count'] for d in top_destinations_qs]

    context = {
        'recent_bookings': recent_bookings,
        'stats': {
            'total_users': User.objects.count(),
            'total_bookings': Booking.objects.count(),
            'total_revenue': total_revenue,
            'packages_count': TourPackage.objects.count(),
        },
        # JSON-encoded chart data (safe to inject into <script> tags)
        'chart_monthly_labels': json.dumps(monthly_labels),
        'chart_monthly_data':   json.dumps(monthly_data),
        'chart_dest_labels':    json.dumps(dest_labels),
        'chart_dest_data':      json.dumps(dest_data),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
