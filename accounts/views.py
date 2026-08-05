from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserProfileForm

def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard:redirect_dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Welcome to AetherVoyage, {user.username}! Account created successfully.")
            return redirect('dashboard:redirect_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome back, {self.request.user.username}!")
        return response

def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Failed to update profile.")
    else:
        form = CustomUserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
