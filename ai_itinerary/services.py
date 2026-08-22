from django.conf import settings
from google import genai

# ---------------------------------------------------------------------------
# Gemini client factory
# ---------------------------------------------------------------------------

def get_gemini_client():
    """
    Returns a configured google.genai.Client, or None if the API key is absent.
    Uses the new google-genai SDK (google.generativeai is deprecated).
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '').strip()
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error creating Gemini client: {e}")
        return None


_MODEL = 'gemini-3.6-flash'


def _clean_html(text: str) -> str:
    """Strip markdown code fences if the model added them."""
    text = text.strip()
    if text.startswith("```html"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


# ---------------------------------------------------------------------------
# Core AI functions
# ---------------------------------------------------------------------------

def generate_itinerary(destination, days, budget, style, interests=""):
    """
    Generates a structured HTML day-by-day travel itinerary via Gemini.
    Falls back to a mock if the API key is missing or the call fails.
    """
    client = get_gemini_client()

    prompt = f"""
    Create a highly professional and realistic travel itinerary for:
    Destination: {destination}
    Duration: {days} days
    Budget level: {budget} (choices: budget, mid-range, luxury)
    Travel style: {style} (choices: adventure, relaxed, cultural, foodie, general)
    Specific interests: {interests}

    Format the itinerary as a clean HTML snippet (no ```html wrapper — just raw HTML tags).
    Rules:
    1. Organize day-by-day with <h3>Day X: [Title]</h3>.
    2. Under each day provide:
       - <strong>Morning:</strong> [Activity and tips]
       - <strong>Afternoon:</strong> [Activity and tips]
       - <strong>Evening:</strong> [Activity and tips]
       - <strong>Estimated Expenses:</strong> [Brief USD cost breakdown for the day]
    3. No emojis, no neon decorations. Read like a premium travel brochure.
    4. Keep it dense in information and realistic.
    """

    if not client:
        return get_mock_itinerary(destination, days, budget, style, interests)

    try:
        response = client.models.generate_content(model=_MODEL, contents=prompt)
        return _clean_html(response.text)
    except Exception as e:
        print(f"Gemini itinerary error: {e}")
        return get_mock_itinerary(destination, days, budget, style, interests)


def generate_budget_estimate(destination, days, style):
    """
    Generates an HTML budget summary for the trip.
    """
    client = get_gemini_client()

    prompt = f"""
    Provide a detailed travel budget estimation for:
    Destination: {destination}
    Duration: {days} days
    Style: {style}

    Write a concise summary in HTML format (using simple <p>, <ul>, and <li> tags) covering:
    - Accommodation costs
    - Food & Dining costs
    - Transportation costs
    - Sightseeing & Activities costs
    Make values realistic for {destination}. No emojis or markdown code blocks.
    """

    if not client:
        return _mock_budget(destination, days, style)

    try:
        response = client.models.generate_content(model=_MODEL, contents=prompt)
        return _clean_html(response.text)
    except Exception as e:
        print(f"Gemini budget error: {e}")
        return "<p>Budget estimation is temporarily unavailable. Please try again later.</p>"


def generate_packing_list(destination, days, style):
    """
    Generates an HTML packing checklist for the trip.
    """
    client = get_gemini_client()

    prompt = f"""
    Generate a practical packing checklist for a {days}-day trip to {destination} with a travel style of {style}.
    Return the checklist in HTML format (using <ul> and <li> tags only). Keep it concise, professional, and practical.
    No emojis, no markdown code blocks.
    """

    if not client:
        return _mock_packing(destination, style)

    try:
        response = client.models.generate_content(model=_MODEL, contents=prompt)
        return _clean_html(response.text)
    except Exception as e:
        print(f"Gemini packing error: {e}")
        return "<p>Packing checklist is temporarily unavailable. Please try again later.</p>"


def get_chatbot_reply(user_message, history=None):
    """
    Returns a chatbot reply from the Travel Assistant via Gemini.
    history: list of ChatHistory model instances (with .message / .response fields).
    """
    if history is None:
        history = []

    client = get_gemini_client()

    # Build conversation context from last 5 exchanges
    history_context = ""
    for msg in history[-5:]:
        history_context += f"User: {msg.message}\nAssistant: {msg.response}\n"

    prompt = f"""
    You are the "Travel Assistant" for AetherVoyage, a premium travel company.
    Be polite, helpful, clear, and professional. Do NOT use emojis. Keep responses under 120 words.

    Conversation history:
    {history_context}

    User message: {user_message}
    """

    if not client:
        return get_mock_chatbot_response(user_message)

    try:
        response = client.models.generate_content(model=_MODEL, contents=prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini chatbot error: {e}")
        return get_mock_chatbot_response(user_message)


# ---------------------------------------------------------------------------
# Mock / fallback generators
# ---------------------------------------------------------------------------

def get_mock_itinerary(destination, days, budget, style, interests=""):
    html = ""
    for d in range(1, int(days) + 1):
        daily_budget = '50' if budget == 'budget' else '120' if budget == 'mid_range' else '300'
        html += f"""
        <div class="mb-4 border-bottom pb-3">
            <h5 class="brand-font text-primary">Day {d}: Exploring the Heart of {destination}</h5>
            <p class="small mb-2"><strong>Morning:</strong> Start your day with a local breakfast at a guesthouse. Embark on a guided walking tour covering key historical and scenic landmarks suited for {style} travel.</p>
            <p class="small mb-2"><strong>Afternoon:</strong> Enjoy lunch at a traditional diner. Continue with your customized activity focusing on: "{interests or 'local sights'}" with plenty of time for photography.</p>
            <p class="small mb-2"><strong>Evening:</strong> Unwind with dinner at a highly rated local tavern, followed by a walk along the illuminated streets.</p>
            <p class="small mb-0 text-accent"><strong>Estimated Expenses:</strong> ${daily_budget} USD (Includes meals, transit, and admissions)</p>
        </div>
        """
    return html


def _mock_budget(destination, days, style):
    return f"""
    <p><strong>Estimated Budget Summary for {destination} ({days} Days, {style} style):</strong></p>
    <ul>
        <li><strong>Accommodation:</strong> $80 – $150 per night (Mid-range hotel/guesthouse)</li>
        <li><strong>Meals &amp; Dining:</strong> $30 – $60 per day (Local cafes &amp; mid-range restaurants)</li>
        <li><strong>Local Transportation:</strong> $10 – $25 per day (Public transit / occasional taxi)</li>
        <li><strong>Activities:</strong> $15 – $40 per day (Excursions &amp; museum entries)</li>
    </ul>
    <p><em>Total Suggested Daily Budget: $135 – $275 USD per traveler.</em></p>
    """


def _mock_packing(destination, style):
    return f"""
    <p><strong>Recommended Packing Checklist:</strong></p>
    <ul>
        <li>Comfortable walking shoes suitable for {style} activities</li>
        <li>Lightweight, breathable clothing layers</li>
        <li>Weather-appropriate outerwear (jacket/umbrella)</li>
        <li>Personal toiletries and prescription medications</li>
        <li>Travel document organizer (Passport, insurance, booking confirmations)</li>
        <li>Universal power adapter &amp; charging cables</li>
    </ul>
    """


def get_mock_chatbot_response(message):
    message_lower = message.lower()
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I am your AetherVoyage Travel Assistant. How can I help you check packages, review bookings, or plan your next trip today?"
    elif any(word in message_lower for word in ['booking', 'book', 'reserve']):
        return "To book a trip, navigate to our Packages page, select your desired destination, and click 'Book This Trip'. Our staff will review and approve your request shortly."
    elif any(word in message_lower for word in ['itinerary', 'plan', 'planner']):
        return "You can generate custom day-by-day travel planners using our AI Planner tool. Just select your destination, days, budget, and travel style."
    else:
        return f"Thank you for your question. For bookings, please browse our active packages. For custom schedules, head over to the AI Itinerary Planner page."
