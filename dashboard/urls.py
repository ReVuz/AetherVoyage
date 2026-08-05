from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.redirect_dashboard, name='redirect_dashboard'),
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]
