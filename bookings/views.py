from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import staff_required, customer_required
from packages.models import TourPackage
from .models import Booking

@login_required
@customer_required
def booking_checkout(request, package_id):
    """
    Handles trip booking checkout, traveler inputs, slot verification, and price calculations.
    """
    package = get_object_or_404(TourPackage, pk=package_id, is_active=True)
    
    if package.available_slots <= 0:
        messages.error(request, "This tour package is unfortunately sold out.")
        return redirect('packages:package_detail', pk=package.id)

    if request.method == 'POST':
        try:
            number_of_travelers = int(request.POST.get('number_of_travelers', 1))
            if number_of_travelers <= 0:
                raise ValueError()
        except ValueError:
            messages.error(request, "Please enter a valid positive number of travelers.")
            return render(request, 'bookings/booking_checkout.html', {'package': package})

        if number_of_travelers > package.available_slots:
            messages.error(request, f"Cannot book {number_of_travelers} slots. Only {package.available_slots} slots are available.")
            return render(request, 'bookings/booking_checkout.html', {'package': package})

        special_requests = request.POST.get('special_requests', '').strip()
        
        # Calculate total price
        total_price = package.price * number_of_travelers
        
        # Create Booking
        booking = Booking.objects.create(
            user=request.user,
            package=package,
            number_of_travelers=number_of_travelers,
            total_price=total_price,
            special_requests=special_requests,
            status='pending'
        )
        
        # Subtract from available slots
        package.available_slots -= number_of_travelers
        package.save()
        
        messages.success(request, f"Booking for {package.title} created successfully! Pending staff approval.")
        return redirect('dashboard:customer_dashboard')
        
    return render(request, 'bookings/booking_checkout.html', {'package': package})

@login_required
def cancel_booking(request, booking_id):
    """
    Allows a customer to cancel their own booking, or staff to cancel any booking.
    """
    booking = get_object_or_404(Booking, pk=booking_id)
    
    # Check permissions: user must own booking or be staff
    if booking.user != request.user and not request.user.is_staff and request.user.role != 'admin':
        messages.error(request, "You do not have permission to cancel this booking.")
        return redirect('dashboard:redirect_dashboard')
        
    if booking.status == 'cancelled':
        messages.warning(request, "This booking has already been cancelled.")
        return redirect('dashboard:redirect_dashboard')
        
    # Cancel and restore slots
    booking.status = 'cancelled'
    booking.save()
    
    booking.package.available_slots += booking.number_of_travelers
    booking.package.save()
    
    messages.success(request, f"Booking #{booking.id} has been cancelled and slots restored.")
    return redirect('dashboard:redirect_dashboard')

@login_required
@staff_required
def approve_booking(request, booking_id):
    """
    Staff/Admin action to approve a pending booking.
    """
    booking = get_object_or_404(Booking, pk=booking_id)
    
    if booking.status != 'pending':
        messages.warning(request, f"Booking is already in '{booking.status}' state.")
        return redirect('dashboard:redirect_dashboard')
        
    booking.status = 'approved'
    booking.save()
    
    messages.success(request, f"Booking #{booking.id} has been approved.")
    return redirect('dashboard:redirect_dashboard')

@login_required
@staff_required
def reject_booking(request, booking_id):
    """
    Staff/Admin action to reject a pending booking (marks as cancelled and restores slots).
    """
    booking = get_object_or_404(Booking, pk=booking_id)
    
    if booking.status != 'pending':
        messages.warning(request, f"Booking is already in '{booking.status}' state.")
        return redirect('dashboard:redirect_dashboard')
        
    booking.status = 'cancelled'
    booking.save()
    
    # Restore slots
    booking.package.available_slots += booking.number_of_travelers
    booking.package.save()
    
    messages.success(request, f"Booking #{booking.id} has been rejected/cancelled and slots restored.")
    return redirect('dashboard:redirect_dashboard')
