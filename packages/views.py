from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from accounts.decorators import staff_required, customer_required
from .models import Destination, TourPackage, Review
from .forms import DestinationForm, TourPackageForm, ReviewForm

def homepage(request):
    """
    Renders the main travel agency homepage.
    """
    # Fetch active packages and calculate average rating
    packages = TourPackage.objects.filter(is_active=True).annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-created_at')[:4]
    
    # Fetch destinations
    destinations = Destination.objects.all().order_by('-created_at')[:4]
    
    # Fetch a few reviews to show on homepage
    recent_reviews = Review.objects.all().select_related('user', 'package').order_by('-created_at')[:3]
    
    context = {
        'packages': packages,
        'destinations': destinations,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'packages/homepage.html', context)

def package_list(request):
    """
    Lists packages with search filters and sorting.
    """
    query_set = TourPackage.objects.filter(is_active=True).annotate(
        avg_rating=Avg('reviews__rating')
    )
    
    # Get parameters
    q = request.GET.get('q', '').strip()
    destination_id = request.GET.get('destination', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    min_duration = request.GET.get('min_duration', '')
    max_duration = request.GET.get('max_duration', '')
    available_only = request.GET.get('available_only', '')
    sort_by = request.GET.get('sort', 'date_asc')
    
    # Apply Filters
    if q:
        query_set = query_set.filter(
            Q(title__icontains=q) | 
            Q(description__icontains=q) |
            Q(destination__name__icontains=q) |
            Q(destination__location__icontains=q)
        )
        
    if destination_id:
        query_set = query_set.filter(destination_id=destination_id)
        
    if min_price:
        try:
            query_set = query_set.filter(price__gte=float(min_price))
        except ValueError:
            pass
            
    if max_price:
        try:
            query_set = query_set.filter(price__lte=float(max_price))
        except ValueError:
            pass
            
    if min_duration:
        try:
            query_set = query_set.filter(duration_days__gte=int(min_duration))
        except ValueError:
            pass
            
    if max_duration:
        try:
            query_set = query_set.filter(duration_days__lte=int(max_duration))
        except ValueError:
            pass
            
    if available_only == 'on':
        query_set = query_set.filter(available_slots__gt=0)
        
    # Apply Sorting
    if sort_by == 'price_asc':
        query_set = query_set.order_by('price')
    elif sort_by == 'price_desc':
        query_set = query_set.order_by('-price')
    elif sort_by == 'duration_asc':
        query_set = query_set.order_by('duration_days')
    elif sort_by == 'duration_desc':
        query_set = query_set.order_by('-duration_days')
    elif sort_by == 'date_asc':
        query_set = query_set.order_by('start_date')
    else:
        query_set = query_set.order_by('start_date')
        
    destinations = Destination.objects.all().order_by('name')
    
    context = {
        'packages': query_set,
        'destinations': destinations,
        'filters': {
            'q': q,
            'destination': destination_id,
            'min_price': min_price,
            'max_price': max_price,
            'min_duration': min_duration,
            'max_duration': max_duration,
            'available_only': available_only,
            'sort': sort_by
        }
    }
    return render(request, 'packages/package_list.html', context)

def package_detail(request, pk):
    """
    Renders package detail page, reviews list, and review form.
    """
    package = get_object_or_404(
        TourPackage.objects.annotate(avg_rating=Avg('reviews__rating')), 
        pk=pk
    )
    reviews = package.reviews.all().select_related('user')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to submit a review.")
            return redirect('accounts:login')
        
        # Verify role (only customers can write reviews)
        if request.user.role != 'customer' and not request.user.is_superuser:
            messages.error(request, "Only customers can submit package reviews.")
            return redirect('packages:package_detail', pk=pk)
            
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.package = package
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been posted successfully!")
            return redirect('packages:package_detail', pk=pk)
        else:
            messages.error(request, "Failed to submit review. Please try again.")
    else:
        form = ReviewForm()
        
    context = {
        'package': package,
        'reviews': reviews,
        'form': form
    }
    return render(request, 'packages/package_detail.html', context)


# STAFF & ADMIN CRUD MANAGEMENT VIEWS

@login_required
@staff_required
def manage_packages(request):
    """
    Operational landing page for staff and admin to see list of destinations and packages.
    """
    packages = TourPackage.objects.all().select_related('destination').annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-created_at')
    
    destinations = Destination.objects.all().order_by('-created_at')
    
    context = {
        'packages': packages,
        'destinations': destinations
    }
    return render(request, 'packages/manage_packages.html', context)

@login_required
@staff_required
def add_destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Destination created successfully.")
            return redirect('packages:manage_packages')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DestinationForm()
    return render(request, 'packages/destination_form.html', {'form': form, 'title': 'Add Destination'})

@login_required
@staff_required
def edit_destination(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            messages.success(request, "Destination updated successfully.")
            return redirect('packages:manage_packages')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'packages/destination_form.html', {'form': form, 'title': f'Edit Destination: {destination.name}'})

@login_required
@staff_required
def delete_destination(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.delete()
        messages.success(request, "Destination deleted successfully.")
        return redirect('packages:manage_packages')
    return render(request, 'packages/confirm_delete.html', {'object': destination, 'type': 'Destination'})

@login_required
@staff_required
def add_package(request):
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Tour Package created successfully.")
            return redirect('packages:manage_packages')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TourPackageForm()
    return render(request, 'packages/package_form.html', {'form': form, 'title': 'Add Tour Package'})

@login_required
@staff_required
def edit_package(request, pk):
    package = get_object_or_404(TourPackage, pk=pk)
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, "Tour Package updated successfully.")
            return redirect('packages:manage_packages')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TourPackageForm(instance=package)
    return render(request, 'packages/package_form.html', {'form': form, 'title': f'Edit Package: {package.title}'})

@login_required
@staff_required
def delete_package(request, pk):
    package = get_object_or_404(TourPackage, pk=pk)
    if request.method == 'POST':
        package.delete()
        messages.success(request, "Tour Package deleted successfully.")
        return redirect('packages:manage_packages')
    return render(request, 'packages/confirm_delete.html', {'object': package, 'type': 'Tour Package'})
