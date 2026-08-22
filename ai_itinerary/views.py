import io
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa

from .models import SavedItinerary, ChatHistory
from . import services

@login_required
def itinerary_planner(request):
    """
    Renders the AI Travel Planner form and handles generation requests.
    """
    if request.method == 'POST':
        destination = request.POST.get('destination', '').strip()
        try:
            duration_days = int(request.POST.get('duration_days', 3))
            if duration_days <= 0 or duration_days > 14:
                raise ValueError()
        except ValueError:
            messages.error(request, "Please enter a valid number of days (1 to 14).")
            return render(request, 'ai_itinerary/itinerary_planner.html')

        budget_category = request.POST.get('budget_category', 'mid_range')
        travel_style = request.POST.get('travel_style', 'general')
        interests = request.POST.get('interests', '').strip()

        if not destination:
            messages.error(request, "Please enter a valid destination.")
            return render(request, 'ai_itinerary/itinerary_planner.html')

        # Generate using Gemini service
        messages.info(request, f"Generating custom travel plan for {destination}...")
        itinerary_content = services.generate_itinerary(
            destination, duration_days, budget_category, travel_style, interests
        )
        budget_estimate = services.generate_budget_estimate(
            destination, duration_days, travel_style
        )
        packing_list = services.generate_packing_list(
            destination, duration_days, travel_style
        )

        # Save to Database
        itinerary = SavedItinerary.objects.create(
            user=request.user,
            destination=destination,
            duration_days=duration_days,
            budget_category=budget_category,
            travel_style=travel_style,
            interests=interests,
            itinerary_content=itinerary_content,
            budget_estimate=budget_estimate,
            packing_list=packing_list
        )

        messages.success(request, f"Successfully created your itinerary for {destination}!")
        return redirect('ai_itinerary:itinerary_detail', pk=itinerary.pk)

    return render(request, 'ai_itinerary/itinerary_planner.html')

@login_required
def itinerary_list(request):
    """
    Lists itineraries saved by the current customer.
    """
    itineraries = SavedItinerary.objects.filter(user=request.user)
    return render(request, 'ai_itinerary/itinerary_list.html', {'itineraries': itineraries})

@login_required
def itinerary_detail(request, pk):
    """
    Displays the day-by-day travel brochure, budget advice, and packing lists.
    """
    itinerary = get_object_or_404(SavedItinerary, pk=pk)
    
    # Restrict viewing to the owner
    if itinerary.user != request.user and not request.user.is_staff and not request.user.role == 'admin':
        messages.error(request, "You do not have permission to view this itinerary.")
        return redirect('dashboard:redirect_dashboard')
        
    return render(request, 'ai_itinerary/itinerary_detail.html', {'itinerary': itinerary})

@login_required
def download_itinerary_pdf(request, pk):
    """
    Generates a premium PDF brochure for the saved itinerary.
    The destination cover image is fetched server-side and embedded as
    a base64 data URI so xhtml2pdf can render it without any network call.
    """
    itinerary = get_object_or_404(SavedItinerary, pk=pk)

    # Permission check: only owner, staff, or admin
    if itinerary.user != request.user and not request.user.is_staff and not getattr(request.user, 'role', '') == 'admin':
        return HttpResponse("Unauthorized", status=403)

    # Fetch destination image as an embedded base64 data URI
    cover_image_uri = services.get_destination_image_b64(itinerary.destination)

    context = {
        'itinerary': itinerary,
        'user': request.user,
        'cover_image_uri': cover_image_uri,
    }

    template = get_template('ai_itinerary/itinerary_pdf_template.html')
    html = template.render(context)

    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode('utf-8')), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        safe_dest = itinerary.destination.lower().replace(' ', '_').replace(',', '')
        response['Content-Disposition'] = f'attachment; filename="aethervoyage_{safe_dest}_itinerary.pdf"'
        return response

    return HttpResponse(f"PDF generation failed. Please try again.", status=500)

@login_required
def itinerary_delete(request, pk):
    """
    Deletes a saved itinerary if the user owns it.
    """
    if request.method == 'POST':
        itinerary = get_object_or_404(SavedItinerary, pk=pk)
        if itinerary.user == request.user or request.user.is_staff or request.user.role == 'admin':
            itinerary.delete()
            messages.success(request, "Itinerary deleted successfully.")
        else:
            messages.error(request, "You do not have permission to delete this itinerary.")
    return redirect('ai_itinerary:itinerary_list')

@login_required
@csrf_exempt
def chat_api(request):
    """
    AJAX endpoint for user conversations with the Travel Assistant.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=400)
        
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
        
    if not message:
        return JsonResponse({'error': 'Message is empty'}, status=400)
        
    # Get recent chat history to provide context
    history = ChatHistory.objects.filter(user=request.user).order_by('created_at')[:10]
    
    # Get assistant reply
    reply = services.get_chatbot_reply(message, list(history))
    
    # Save conversation log
    ChatHistory.objects.create(
        user=request.user,
        message=message,
        response=reply
    )
    
    return JsonResponse({'response': reply})

@login_required
def destination_recommendation(request):
    """
    Renders AI Destination Recommendation page and handles generation.
    """
    recommendations = None
    if request.method == 'POST':
        preferences = request.POST.get('preferences', '').strip()
        if preferences:
            recommendations = services.generate_destination_recommendation(preferences)
        else:
            messages.error(request, "Please enter your preferences.")
            
    return render(request, 'ai_itinerary/destination_recommendation.html', {'recommendations': recommendations})

