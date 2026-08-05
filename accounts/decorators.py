from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator for views that checks whether the user has one of the allowed roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, "Please log in to access this page.")
                return redirect('accounts:login')
            
            # Admins (superusers) bypass all role restrictions
            if request.user.is_superuser or request.user.role == 'admin':
                return view_func(request, *args, **kwargs)
                
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, "You do not have permission to view this page.")
            # Redirect to user's dashboard or login page
            return redirect('dashboard:redirect_dashboard')
        return _wrapped_view
    return decorator

def admin_required(view_func):
    return role_required(['admin'])(view_func)

def staff_required(view_func):
    return role_required(['staff', 'admin'])(view_func)

def customer_required(view_func):
    return role_required(['customer'])(view_func)
