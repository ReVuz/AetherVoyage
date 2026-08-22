# AetherVoyage

A premium Django-based travel platform featuring AI-powered itinerary generation, role-based dashboards (Admin, Staff, Customer), booking management, and downloadable PDF brochures.

## Features
- **AI Travel Planner**: Generates day-by-day itineraries, budget estimates, and packing lists via Gemini API.
- **AI Chatbot**: A persistent travel assistant widget.
- **AI Destination Recommendations**: Get recommendations based on user preferences.
- **Role-based Authentication**: Distinct experiences and permissions for Admins, Staff, and Customers.
- **Travel Management & Bookings**: Tour package exploration with complete checkout and staff approval workflow.
- **Interactive Dashboards**: Integrated Chart.js metrics for system administration.
- **PDF Generation**: Export AI itineraries to downloadable PDFs.

## Setup Instructions

1. **Clone the repository** (if not already local).
2. **Set up virtual environment & install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables:**
   Create a `.env` file in the root directory (where `manage.py` is located) with your Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
4. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a Superuser** (to access Django admin and the Admin Dashboard):
   ```bash
   python manage.py createsuperuser
   ```
6. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```
7. **Access the application:**
   Visit `http://127.0.0.1:8000` in your web browser.

## Testing
Run the test suite with:
```bash
python manage.py test
```

## Technologies
Django, Python, Bootstrap 5, SQLite, Gemini AI SDK, xhtml2pdf, Chart.js.
