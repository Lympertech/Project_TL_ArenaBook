# ArenaBook

ArenaBook is a Django web application for searching, booking and managing sports facilities.

## Stack

- Python
- Django
- MySQL local
- Django Templates
- Bootstrap via CDN
- GitHub
- VS Code

Payment handling will be implemented later as a mock flow, with no real external payment integration.

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install requirements:

```powershell
pip install -r requirements.txt
```

This project is configured for `mysqlclient`. On Windows, if installing `mysqlclient` fails because of local build dependencies, PyMySQL can be considered as a fallback later, but it is not configured in this skeleton.

3. Create the local MySQL database and user:

```sql
CREATE DATABASE arenabook_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'arenabook_user'@'localhost' IDENTIFIED BY 'arenabook_password';
GRANT ALL PRIVILEGES ON arenabook_db.* TO 'arenabook_user'@'localhost';
FLUSH PRIVILEGES;
```

4. Create a local environment file:

```powershell
Copy-Item .env.example .env
```

Then fill in `SECRET_KEY` in `.env`.

5. Check the project and create database migrations:

If this local database was migrated before the custom `accounts.User` model was added, recreate the local development database first so the custom user model is part of the initial schema.

```powershell
python manage.py check
```

```powershell
python manage.py makemigrations
```

6. Apply migrations:

```powershell
python manage.py migrate
```

7. Create a Django admin superuser:

```powershell
python manage.py createsuperuser
```

8. Seed demo data:

```powershell
python manage.py seed_demo
```

Demo users created by `seed_demo`:

- `user` / `password123`
- `manager` / `password123`
- `sysadmin` / `password123`

9. Run the development server:

```powershell
python manage.py runserver
```

## Authentication and Roles

The project now includes basic authentication and role-based access guards.

Register a public account at:

```text
http://127.0.0.1:8000/accounts/register/
```

Public registration supports only these roles:

- `USER`
- `FACILITY_MANAGER`

`SYSTEM_ADMIN` users must be created through Django admin or `seed_demo`.

Login at:

```text
http://127.0.0.1:8000/accounts/login/
```

After login or registration, users are redirected by role:

- `USER` -> `/accounts/user/dashboard/`
- `FACILITY_MANAGER` -> `/facilities/manager/`
- `SYSTEM_ADMIN` -> `/facilities/admin-panel/pending/`

## Facility Manager and Admin Workflows

The project now includes basic facility lifecycle and setup workflows:

- UC-10 Submit Facility
- UC-14 Approve Facility Submission
- UC-08 Manage Booking Rules
- UC-09 Manage Cancellation Policy
- UC-11 Create or Update Field
- UC-12 Create or Update Field Slots
- UC-13 Declare Temporary Field Unavailability

Facility managers can submit facilities, view only their own facilities, manage booking rules, manage cancellation policy, create or update fields, create or update field slots, and declare temporary field unavailability for their facilities.

System admins can view pending facility submissions and approve or reject them.

The slot and temporary unavailability workflows include:

- validation that start date and time is before end date and time
- prevention of overlapping slots for the same field
- prevention of slot and unavailability conflicts with confirmed bookings
- duplicate prevention for temporary unavailability periods

## Search and Availability

The project now includes:

- UC-02 Search Facility
- UC-03 View Field Availability

Facility search returns only `ACTIVE` facilities. Users can filter by location, sport type, and optional date.

Field availability is derived from:

- `Slot`
- `Booking`
- `TemporaryUnavailability`

Availability is not stored as a separate model. Confirmed bookings and temporary unavailability periods are excluded from available slots.

Booking creation, payment, booking modification, booking cancellation, tests, and UI polishing will be implemented in later steps after the sequence diagrams and class diagram are verified.
