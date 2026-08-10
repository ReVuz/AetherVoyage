from django.urls import path
from . import views

app_name = 'packages'

urlpatterns = [
    path('', views.package_list, name='package_list'),
    path('<int:pk>/', views.package_detail, name='package_detail'),
    path('manage/', views.manage_packages, name='manage_packages'),
    path('destination/add/', views.add_destination, name='add_destination'),
    path('destination/<int:pk>/edit/', views.edit_destination, name='edit_destination'),
    path('destination/<int:pk>/delete/', views.delete_destination, name='delete_destination'),
    path('add/', views.add_package, name='add_package'),
    path('<int:pk>/edit/', views.edit_package, name='edit_package'),
    path('<int:pk>/delete/', views.delete_package, name='delete_package'),
]
