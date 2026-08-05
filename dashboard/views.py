from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required, staff_required, customer_required

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
    # Retrieve customer-specific data (bookings, saved itineraries)
    # We will expand this once those models are defined
    context = {
        'bookings': [],
        'itineraries': [],
        'stats': {
            'total_bookings': 0,
            'total_spent': 0.0,
            'total_itineraries': 0,
        }
    }
    return render(request, 'dashboard/customer_dashboard.html', context)

@login_required
@staff_required
def staff_dashboard(request):
    # Retrieve staff-specific data (pending bookings, packages count, etc.)
    # We will expand this once those models are defined
    context = {
        'pending_bookings': [],
        'active_packages': [],
        'stats': {
            'pending_count': 0,
            'packages_count': 0,
            'destinations_count': 0,
        }
    }
    return render(request, 'dashboard/staff_dashboard.html', context)

@login_required
@admin_required
def admin_dashboard(request):
    # Retrieve global system stats
    # We will expand this once models are defined
    context = {
        'recent_bookings': [],
        'stats': {
            'total_users': 0,
            'total_bookings': 0,
            'total_revenue': 0.0,
            'packages_count': 0,
        }
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
