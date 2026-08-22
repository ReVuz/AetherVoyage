from django.urls import path
from . import views

app_name = 'ai_itinerary'

urlpatterns = [
    path('planner/', views.itinerary_planner, name='itinerary_planner'),
    path('my-itineraries/', views.itinerary_list, name='itinerary_list'),
    path('my-itineraries/<int:pk>/', views.itinerary_detail, name='itinerary_detail'),
    path('my-itineraries/<int:pk>/pdf/', views.download_itinerary_pdf, name='download_itinerary_pdf'),
    path('my-itineraries/<int:pk>/delete/', views.itinerary_delete, name='itinerary_delete'),
    path('chat/api/', views.chat_api, name='chat_api'),
    path('recommend/', views.destination_recommendation, name='destination_recommendation'),
]
