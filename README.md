# AetherVoyage — AI Travel & Itinerary Planner

**AetherVoyage** is a premium, Django-powered travel platform that allows users to explore destinations and tour packages, purchase bookings, and generate highly customized travel itineraries using AI (Gemini). It features a role-based dashboard system separating duties for Admins, Staff, and Customers.

---

## Current Status (Phases 1-3 Backend)

We are developing the project in phases. Currently, the following components have been fully implemented:

### 1. Phase 1: Project Setup (Completed)
- **Django Core Settings**: Structured clean configurations inside the `aether_voyage` directory, handling media assets, static resources, templates, and SQLite database connections.
- **Environment Management**: Implemented `.env` configuration file reading via `django-environ`.
- **Custom User Model**: Created `CustomUser` in the `accounts` app extending `AbstractUser` with user-facing fields (`role`, `phone_number`, `profile_picture`, `bio`) and custom property checks.
  - Role Choices: `admin`, `staff`, `customer`.

### 2. Phase 2: Authentication & Roles (Completed)
- **Registration and Profiles**: Designed signup and profile edit forms (`CustomUserCreationForm`, `CustomUserProfileForm`).
- **Access Control Decorators**: Developed custom view decorators in `accounts/decorators.py` to handle role restrictions:
  - `@customer_required`
  - `@staff_required`
  - `@admin_required`
- **Dashboard Stub Configurations**: Standardized dashboard view endpoints for roles and custom redirection middleware matching logged-in user credentials.

### 3. Phase 3: Travel Management - Database Models (Completed)
- **Models Design**: Defined the database structures in `packages/models.py`:
  - `Destination`: Tracks cities/regions, descriptions, and media cover photos.
  - `TourPackage`: Tracks pricing, start/end dates, available booking slots, and active states.
  - `Review`: Allows users to post 1-5 star ratings and textual reviews.
- **Admin Configuration**: Registered all models inside `accounts/admin.py` and `packages/admin.py` to configure search, list views, and fieldsets.

---

## Installation & Setup

To run AetherVoyage locally, follow these steps:

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Set Up a Virtual Environment

Navigate to the project root and create a virtual environment (`.venv`) for your operating system:

#### Windows
- **Create**:
  ```cmd
  python -m venv .venv
  ```
- **Activate** (Command Prompt):
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **Activate** (PowerShell):
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **Activate** (Git Bash):
  ```bash
  source .venv/Scripts/activate
  ```

#### Ubuntu / Debian Linux
- **Prerequisite** (if not already installed):
  ```bash
  sudo apt update
  sudo apt install python3-venv
  ```
- **Create**:
  ```bash
  python3 -m venv .venv
  ```
- **Activate**:
  ```bash
  source .venv/bin/activate
  ```

#### macOS
- **Create**:
  ```bash
  python3 -m venv .venv
  ```
- **Activate**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies
After activating the virtual environment, install the required packages:
```bash
pip install -r requirements.txt
```

### 4. Set Up API Credentials
Open the `.env` file in the project root and add your Gemini API key:
```env
DEBUG=True
SECRET_KEY=your-django-secret-key
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Run Migrations & Start Server
Apply database migrations and start the development server:
```bash
# Run migrations
python manage.py migrate

# Start the dev server
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/`.

---

## How to Verify Completed Features

You can check and verify the current codebase using any of the following methods:

### Method A: Automated Test Suite (Recommended)
We have written a comprehensive suite of unit tests to verify role logic, form creation, and decorator authorization:
```bash
python manage.py test
```
*Expected output: All 4 tests pass successfully (`OK`).*

### Method B: Django Interactive Shell
You can verify the CustomUser roles properties in the Django python shell:
```bash
python manage.py shell
```
```python
from accounts.models import CustomUser

# Create test users with different roles
cust = CustomUser.objects.create_user(username='customer_test', role='customer')
stf = CustomUser.objects.create_user(username='staff_test', role='staff')
adm = CustomUser.objects.create_user(username='admin_test', role='admin')

# Validate role checks
print(cust.is_customer)        # True
print(stf.is_staff_member)     # True
print(adm.is_admin)            # True
print(adm.is_staff_member)     # True (Admins have staff permissions)
```

### Method C: Django Admin Panel
1. Create a superuser in the terminal:
   ```bash
   python manage.py createsuperuser
   ```
2. Set their role explicitly in the prompts or update it.
3. Run the development server and navigate to `http://127.0.0.1:8000/admin/`.
4. Log in and verify that you can manage **Custom Users**, **Destinations**, **Tour Packages**, and **Reviews** with full search, sorting, and filtering capabilities.
