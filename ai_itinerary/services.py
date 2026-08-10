import os
import google.generativeai as genai
from django.conf import settings

def get_gemini_model():
    """
    Initializes and returns the Gemini generative model.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        return None
    try:
        genai.configure(api_key=api_key)
        # Using a stable, recommended model
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Error configuring Gemini: {e}")
        return None

def generate_itinerary(destination, days, budget, style, interests=""):
    """
    Generates a day-by-day travel itinerary using the Gemini API.
    Enforces Rule 12: Structured format (Day X -> Morning, Afternoon, Evening, Estimated Expenses).
    """
    model = get_gemini_model()
    
    prompt = f"""
    Create a highly professional and realistic travel itinerary for:
    Destination: {destination}
    Duration: {days} days
    Budget level: {budget} (choices: budget, mid-range, luxury)
    Travel style: {style} (choices: adventure, relaxed, cultural, foodie, general)
    Specific interests: {interests}

    You must format the itinerary as a clean HTML snippet (no ```html wrapper, just the raw HTML tags) adhering to these strict rules:
    1. Organize it day-by-day using <h3>Day X: [Title]</h3>.
    2. Under each day, provide structured headings for:
       - <strong>Morning:</strong> [Activity description and tips]
       - <strong>Afternoon:</strong> [Activity description and tips]
       - <strong>Evening:</strong> [Activity description and tips]
       - <strong>Estimated Expenses:</strong> [Brief breakdown of estimated cost for the day in USD]
    3. Do NOT include any neon glows, futuristic decorations, or emojis in headings. Make it read like a premium travel brochure.
    4. Keep it comfortable to read, dense in information, and realistic.
    """
    
    if not model:
        return get_mock_itinerary(destination, days, budget, style, interests)
        
    try:
        response = model.generate_content(prompt)
        # Clean any markdown wrapper formatting if the model still generated it
        content = response.text.strip()
        if content.startswith("```html"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        return content.strip()
    except Exception as e:
        print(f"Gemini generation error: {e}")
        return get_mock_itinerary(destination, days, budget, style, interests)

def generate_budget_estimate(destination, days, style):
    """
    Generates budget suggestions based on destination, duration, and style.
    """
    model = get_gemini_model()
    
    prompt = f"""
    Provide a detailed travel budget estimation for:
    Destination: {destination}
    Duration: {days} days
    Style: {style}

    Write a concise summary in HTML format (using simple <p>, <ul>, and <li> tags) outlining:
    - Accommodation costs
    - Food & Dining costs
    - Transportation costs
    - Sightseeing & Activities costs
    Make the values realistic for {destination}. No emojis or markdown code blocks.
    """
    
    if not model:
        return f"""
        <p><strong>Estimated Budget Summary for {destination} ({days} Days, {style} style):</strong></p>
        <ul>
            <li><strong>Accommodation:</strong> $80 - $150 per night (Mid-range hotel/guesthouse)</li>
            <li><strong>Meals & Dining:</strong> $30 - $60 per day (Local cafes & mid-range restaurants)</li>
            <li><strong>Local Transportation:</strong> $10 - $25 per day (Public transit / occasional taxi)</li>
            <li><strong>Activities:</strong> $15 - $40 per day (Excursions & museum entries)</li>
        </ul>
        <p><em>Total Suggested Daily Budget: $135 - $275 USD per traveler.</em></p>
        """
        
    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        if content.startswith("```html"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        return content.strip()
    except Exception as e:
        print(f"Gemini budget error: {e}")
        return "<p>Budget estimation is temporarily unavailable. Please try again later.</p>"

def generate_packing_list(destination, days, style):
    """
    Generates a recommended packing checklist.
    """
    model = get_gemini_model()
    
    prompt = f"""
    Generate a practical packing checklist for a {days}-day trip to {destination} for a travel style of {style}.
    Return the checklist in HTML format (using simple <ul> and <li> tags). Keep it concise, professional, and practical.
    """
    
    if not model:
        return f"""
        <p><strong>Recommended Packing Checklist:</strong></p>
        <ul>
            <li>Comfortable walking shoes suitable for {style} activities</li>
            <li>Lightweight, breathable clothing layers</li>
            <li>Weather-appropriate outerwear (jacket/umbrella)</li>
            <li>Personal toiletries and prescription medications</li>
            <li>Travel document organizer (Passport, insurance printouts, booking confirmation PDFs)</li>
            <li>Universal power adapter & charging cables</li>
        </ul>
        """
        
    try:
        response = model.generate_content(prompt)
        content = response.text.strip()
        if content.startswith("```html"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        return content.strip()
    except Exception as e:
        print(f"Gemini packing error: {e}")
        return "<p>Packing checklist is temporarily unavailable. Please try again later.</p>"

def get_chatbot_reply(user_message, history=[]):
    """
    Retrieves responses for the AI assistant chatbot.
    """
    model = get_gemini_model()
    
    # Format chat history context
    history_context = ""
    for msg in history[-5:]:  # limit to last 5 message pairs
        history_context += f"User: {msg.message}\nAssistant: {msg.response}\n"
        
    prompt = f"""
    You are the "Travel Assistant" for AetherVoyage, a premium travel company.
    Your tone should be polite, helpful, clear, and professional. Do NOT use emojis, and do NOT use enthusiastic tags like "AI Magic".
    Keep your response concise (under 120 words).
    
    Context History:
    {history_context}
    
    User message: {user_message}
    """
    
    if not model:
        return get_mock_chatbot_response(user_message)
        
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini chatbot error: {e}")
        return get_mock_chatbot_response(user_message)

def get_mock_itinerary(destination, days, budget, style, interests=""):
    """
    Fallback mock itinerary generator.
    """
    html_content = ""
    for d in range(1, int(days) + 1):
        html_content += f"""
        <div class="mb-4 border-bottom pb-3">
            <h5 class="brand-font text-primary">Day {d}: Exploring the Heart of {destination}</h5>
            <p class="small mb-2"><strong>Morning:</strong> Start your day with a local breakfast at a guesthouse. Embark on a guided walking tour covering key historical and scenic landmarks suited for {style} travel.</p>
            <p class="small mb-2"><strong>Afternoon:</strong> Enjoy lunch at a traditional diner. Continue with your customized activity focusing on: "{interests or 'local sights'}" with plenty of time for photography.</p>
            <p class="small mb-2"><strong>Evening:</strong> Unwind with dinner at a highly rated local tavern, followed by a walk along the illuminated streets and riversides.</p>
            <p class="small mb-0 text-accent"><strong>Estimated Expenses:</strong> ${'50' if budget == 'budget' else '120' if budget == 'mid_range' else '300'} USD (Includes meals, transit, and admissions)</p>
        </div>
        """
    return html_content

def get_mock_chatbot_response(message):
    message_lower = message.lower()
    if 'hello' in message_lower or 'hi' in message_lower:
        return "Hello! I am your AetherVoyage Travel Assistant. How can I help you check packages, review bookings, or plan your next trip today?"
    elif 'booking' in message_lower or 'book' in message_lower:
        return "To book a trip, navigate to our Packages page, select your desired destination, and click 'Book This Trip' in the booking drawer. Our staff will review and approve your request shortly."
    elif 'itinerary' in message_lower or 'plan' in message_lower:
        return "You can generate custom day-by-day travel planners using our AI Planner tool. Just select your destination, days, budget, and travel style to generate a travel brochure."
    else:
        return f"Thank you for asking about '{message}'. I'd be happy to help. For bookings, please browse our active packages. If you want custom schedules, head over to the AI Itinerary page."
