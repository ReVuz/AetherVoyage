# Django AI Travel & Itinerary Planner - Implementation Plan

This project is a premium, Django-based web application called **AetherVoyage** that allows users to explore destinations and tour packages, book trips, and generate fully customized travel itineraries using AI (Gemini/OpenAI). It includes role-based access for Admins, Staff, and Customers, interactive stats dashboards, automated booking workflows, a persistent AI travel assistant chatbot, budget and packing estimators, and downloadable PDF itineraries.

---

## User Review Required

We need your review and input on the following points:

> [!IMPORTANT]
> **1. AI Model Provider & Credentials**
> We plan to default to the **Gemini API** (using the `google-generativeai` package) for AI itinerary generation, recommendations, budget planning, packing lists, and the chatbot because it is highly performant and accessible. However, we can also support **OpenAI API** if preferred. Please ensure you have an API key ready for the selected service.
>
> **2. PDF Generation Library**
> We propose using `xhtml2pdf` to render HTML templates directly into downloadable PDFs. If you have another preference (such as `WeasyPrint` which requires system-level libraries, or raw `ReportLab`), please let us know.
>
> **3. UI Customization & Bootstrap**
> To satisfy the "Bootstrap" requirement while delivering a **premium, wow-factor design**, we will use Bootstrap 5 via CDN for structure, overlaid with a custom styling system (`theme.css`) implementing dark-mode support, glassmorphism, modern typography (Plus Jakarta Sans/Inter), and smooth micro-animations.

---

## Open Questions

> [!NOTE]
> * **API Key Storage:** We will load the Gemini/OpenAI API key from a `.env` file via `django-environ`. Do you have a preferred hosting/deployment target (e.g., Render, Heroku) that requires specific env configuration?
> * **Payment Gateway:** The prompt details booking creation, updates, and approval workflows. Is a mock payment gateway required for bookings, or should it proceed directly to booking confirmation and staff approval? (We recommend a mock payment checkout screen to make the flow feel premium and complete).

---

## Proposed Changes

We will initialize a clean, modern Django project structure in the workspace directory `/home/hp/Documents/final-project-momo`.

### 1. Core Project Infrastructure

We will set up the main Django project config, including settings for templates, static files, media handling, database configuration (SQLite), environment variable loading, and root URL routing.

#### [NEW] [requirements.txt](file:///home/hp/Documents/final-project-momo/requirements.txt)
Defines all python dependencies:
- `Django>=5.0`
- `django-environ` (for environment variable loading)
- `google-generativeai` (Gemini API client)
- `openai` (optional fallback)
- `pillow` (for destination and package image uploads)
- `xhtml2pdf` (for PDF generation)

#### [NEW] [settings.py](file:///home/hp/Documents/final-project-momo/aether_voyage/settings.py)
Django configuration:
- Setup custom user model: `AUTH_USER_MODEL = 'accounts.CustomUser'`
- Set up directories for templates (`templates/`), static files (`static/`), and media (`media/`)
- Enable messages framework and session configurations
- Configure SQLite database
- Configure security settings and static assets settings for production-readiness

#### [NEW] [urls.py](file:///home/hp/Documents/final-project-momo/aether_voyage/urls.py)
Root URL routing mapping routes to the respective apps: `accounts`, `packages`, `bookings`, `ai_itinerary`, and `dashboard`. Includes media asset configuration for development.

---

### 2. Accounts App (`accounts`)

Handles custom user roles (Admin, Staff, Customer), user profiles, login, signup, logout, and permissions.

#### [NEW] [models.py](file:///home/hp/Documents/final-project-momo/accounts/models.py)
- `CustomUser` inheriting from `AbstractUser` with fields:
  - `role`: CharField with choices `admin`, `staff`, `customer`. Defaults to `customer`.
  - `phone_number`: CharField (optional)
  - `profile_picture`: ImageField (optional)
  - `bio`: TextField (optional)

#### [NEW] [forms.py](file:///home/hp/Documents/final-project-momo/accounts/forms.py)
Custom forms for registration (`CustomUserCreationForm`) and profile updates (`CustomUserProfileForm`).

#### [NEW] [views.py](file:///home/hp/Documents/final-project-momo/accounts/views.py)
Auth controller views: signup, login (with redirect based on role), logout, and profile settings.

#### [NEW] [urls.py](file:///home/hp/Documents/final-project-momo/accounts/urls.py)
URL patterns for registration, login, logout, and profile management.

---

### 3. Packages App (`packages`)

Manages destinations and tour packages CRUD, search filters, detail pages, and customer reviews.

#### [NEW] [models.py](file:///home/hp/Documents/final-project-momo/packages/models.py)
- `Destination`: `name`, `description`, `image`, `location`, `created_at`.
- `TourPackage`: `destination` (ForeignKey), `title`, `description`, `price`, `duration_days`, `start_date`, `end_date`, `max_slots`, `available_slots`, `image`, `is_active`, `created_at`.
- `Review`: `package` (ForeignKey), `user` (ForeignKey to CustomUser), `rating` (1 to 5), `comment`, `created_at`.

#### [NEW] [views.py](file:///home/hp/Documents/final-project-momo/packages/views.py)
- Tour packages list & details (with interactive search, price ranges, and duration filters)
- CRUD views for Admin/Staff (Create, Read, Update, Delete destinations and packages)
- Submission endpoint for package reviews (Customer-only role checking)

#### [NEW] [forms.py](file:///home/hp/Documents/final-project-momo/packages/forms.py)
- ModelForms for `Destination`, `TourPackage`, and `Review`.

#### [NEW] [urls.py](file:///home/hp/Documents/final-project-momo/packages/urls.py)
URL mapping for package browsing, detail, review submission, and CRUD operations.

---

### 4. Bookings App (`bookings`)

Handles booking creation, modifications, cancellation, status updates, and staff approval workflow.

#### [NEW] [models.py](file:///home/hp/Documents/final-project-momo/bookings/models.py)
- `Booking`: `user` (ForeignKey), `package` (ForeignKey), `number_of_travelers`, `total_price`, `status` (`pending`, `approved`, `cancelled`), `booking_date`, `special_requests`.

#### [NEW] [views.py](file:///home/hp/Documents/final-project-momo/bookings/views.py)
- Booking creation checkout (calculates total price dynamically, verifies slot availability)
- Booking cancellation and updates (Customer view)
- Booking review & approval/rejection panel (Staff/Admin views)
- Booking history list

#### [NEW] [urls.py](file:///home/hp/Documents/final-project-momo/bookings/urls.py)
URL configurations for booking endpoints.

---

### 5. AI Itinerary & Extra AI Features App (`ai_itinerary`)

The intelligence hub of the application. Integrates with Gemini API to generate travel plans, budget recommendations, packing lists, and host an AI chatbot.

#### [NEW] [models.py](file:///home/hp/Documents/final-project-momo/ai_itinerary/models.py)
- `SavedItinerary`: `user` (ForeignKey), `destination`, `duration_days`, `budget_category` (e.g. Luxury, Budget, Mid-range), `travel_style` (e.g. Adventure, Relaxed, Cultural), `interests` (TextField), `itinerary_content` (TextField/Markdown format generated by Gemini), `budget_estimate` (TextField, generated by Gemini), `packing_list` (TextField, generated by Gemini), `created_at`.
- `ChatHistory`: `user` (ForeignKey), `message`, `response`, `created_at`.

#### [NEW] [services.py](file:///home/hp/Documents/final-project-momo/ai_itinerary/services.py)
API connector module wrapping Gemini prompts:
- `generate_itinerary(destination, days, budget, style, interests) -> dict`
- `generate_budget_estimate(destination, days, style) -> str`
- `generate_packing_list(destination, days, season) -> str`
- `get_chatbot_reply(user_message, history=[]) -> str`

#### [NEW] [views.py](file:///home/hp/Documents/final-project-momo/ai_itinerary/views.py)
- Itinerary creator dashboard & form.
- Saved itineraries browser & details view.
- PDF generation endpoint (renders itinerary to high-quality printable CSS format, converts to PDF via `xhtml2pdf` for download).
- AJAX chatbot endpoint for continuous conversation.

#### [NEW] [urls.py](file:///home/hp/Documents/final-project-momo/ai_itinerary/urls.py)
Routing configurations for AI generation, saved lists, PDF downloads, and chatbot chat requests.

---

### 6. Dashboard App (`dashboard`)

Consolidates metrics and roles permissions, providing tailored portals for Admins, Staff, and Customers.

#### [NEW] [views.py](file:///home/hp/Documents/final-project-momo/dashboard/views.py)
- `Customer Dashboard`: Displays active bookings, saved itineraries, review history, and travel statistics.
- `Staff Dashboard`: Displays pending bookings to approve, booking success rates, active tour packages, and destination listings.
- `Admin Dashboard`: Consolidated view of all site transactions, booking statistics, customer counts, package revenues, and direct link actions.
- Uses `Chart.js` via CDN to display booking distribution, monthly revenue, and destinations popularity charts.

#### [NEW] [urls.py](file:///home/hp/Documents/final-project-momo/dashboard/urls.py)
Routes to dashboards.

---

### 7. Core Premium Templates & Static Assets

Fulfills the visual excellence guidelines by producing a beautiful, modern design.

#### [NEW] [base.html](file:///home/hp/Documents/final-project-momo/templates/base.html)
Global layout featuring:
- Responsive navigation bar with Role status badges and profile dropdown.
- Beautiful, non-intrusive notification banners (using Django messages framework).
- Bottom-right floating AI Assistant widget (expands to a sleek chat panel).
- Modern font embedding (Google Fonts: Plus Jakarta Sans / Inter).

#### [NEW] [custom.css](file:///home/hp/Documents/final-project-momo/static/css/custom.css)
Premium stylesheet styling:
- Glassmorphic card layouts (`backdrop-filter`, subtle borders).
- Curated color palette (Deep space indigo backdrop, electric violet and warm coral gradients, soft amber warning tones).
- Smooth hover animations and custom transition variables.
- Elegant skeletal loading state placeholders for AI operations.

---

## Verification Plan

### Automated Tests
We will add automated tests to verify model structures, booking state changes, and role permissions.
- Run `python manage.py test` to execute:
  - Custom user role verification tests.
  - CRUD access checks (e.g. Customers blocked from creating/updating/deleting packages).
  - Booking slot subtraction checks.

### Manual Verification & Playbook
1. **Interactive Demo Run:**
   - Execute `python manage.py runserver` and navigate to the application using the browser subagent.
2. **Role Verification:**
   - Create accounts for:
     1. Admin (`admin@momo.com`)
     2. Staff (`staff@momo.com`)
     3. Customer (`customer@momo.com`)
   - Verify page routing access for each role (e.g. check that staff can access package editing but customers receive a 403 Forbidden).
3. **AI Generation Check:**
   - Run a test prompt through the Itinerary Generator (e.g., "7 Days in Kyoto, Japan, Luxury, Cultural Interests").
   - Validate response output, save it, and download the generated PDF.
4. **Chatbot Interactive Session:**
   - Ask the chatbot: "What are the top things to do in Paris?" and verify its interactive responses.
