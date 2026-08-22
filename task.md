# AetherVoyage - Development Task List

## Phase 1: Project Setup
- [x] Set up virtual environment and install python dependencies
- [x] Create Django project `aether_voyage` and initialize apps: `accounts`, `packages`, `bookings`, `ai_itinerary`, `dashboard`
- [x] Create custom user model with roles (`admin`, `staff`, `customer`) in `accounts`
- [x] Configure `settings.py` (database, templates, static/media files, auth settings)
- [x] Run initial migrations

## Phase 2: Authentication & Roles
- [x] Implement signup, login, and logout views and forms
- [x] Set up role-based redirect logic (different dashboards for Admin, Staff, and Customer)
- [x] Create access decorators and mixins for role-based views

## Phase 3: Travel Management
- [x] Build models: `Destination`, `TourPackage`, and `Review`
- [x] Create django-admin panels for managing destinations and packages
- [x] Build CRUD views for destinations and tour packages (accessible by Staff/Admin)
- [x] Implement list and details views for packages (accessible by Customer) with search and filters

## Phase 4: Booking System
- [x] Build `Booking` model
- [x] Implement booking creation checkout form (dynamic price calculations, availability checks)
- [x] Create booking cancellation/updates for customers
- [x] Build approval workflow and status management for Staff/Admin

## Phase 5: AI Itinerary Module
- [x] Design travel preferences form (destination, days, budget tier, travel style, interests)
- [x] Implement Gemini API connector service for generating structured itinerary
- [x] Create view to generate, display, and save custom itineraries to the database

## Phase 6: Extra AI Features
- [ ] Implement AI Destination Recommendation feature
- [x] Implement AI Travel Budget Estimator
- [x] Implement AI Packing List Generator
- [x] Build a floating AI Travel Chatbot sidebar widget with AJAX endpoints

## Phase 7: Dashboards & UI Polish
- [x] Create Customer Dashboard (recent bookings, saved itineraries, review history)
- [x] Create Staff Dashboard (pending bookings, packages list, dest list)
- [x] Create Admin Dashboard (aggregate stats: total bookings, total revenue, user count)
- [ ] Integrate Chart.js in dashboards for visualization
- [x] Design premium, fully responsive Bootstrap-based UI with bespoke custom stylesheets and CSS animations

## Phase 8: Finalization & Verification
- [x] Implement downloadable PDF itineraries using `xhtml2pdf`
- [x] Write and run automated tests for role permissions and model relationships
- [ ] Write final README with documentation and setup instructions
