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

Payment and refund handling are mock flows, with no real external payment integration.

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

Open:

```text
http://127.0.0.1:8000/
```

Useful verification commands:

```powershell
python manage.py check
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

## Local Network Demo

For a same Wi-Fi/LAN demo, add your local IPv4 address to `.env`.

Example:

```env
ALLOWED_HOSTS=127.0.0.1,localhost,192.168.1.45
```

Find your local IPv4 address on Windows:

```powershell
ipconfig
```

Start the server on all local network interfaces:

```powershell
python manage.py runserver 0.0.0.0:8000
```

Other devices on the same network can open:

```text
http://YOUR_LOCAL_IP:8000/
```

This is only for local demo/development, not production deployment. If Windows Firewall blocks access, allow Python/Django through the firewall or allow port `8000` temporarily.

## Implemented Use Cases

- UC-01 Register User
- UC-02 Search Facility
- UC-03 View Field Availability
- UC-04 Create Pending Booking
- UC-05 Pay Pending Booking
- UC-06 Modify Confirmed Booking
- UC-07 Cancel Confirmed Booking
- UC-08 Manage Booking Rules
- UC-09 Manage Cancellation Policy
- UC-10 Submit Facility
- UC-11 Create or Update Field
- UC-12 Create or Update Field Slots
- UC-13 Declare Temporary Field Unavailability
- UC-14 Approve Facility Submission

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

## Booking and Mock Payment

The project now includes:

- UC-04 Create Pending Booking
- UC-05 Pay Pending Booking

Users can create a booking from an available slot. New bookings are created with status `PENDING`.

Payment is implemented as a mock flow:

- successful mock payment creates a `SUCCESSFUL` initial payment and changes the booking to `CONFIRMED`
- failed mock payment creates a `FAILED` initial payment and keeps the booking `PENDING`

There is no real external payment integration.

## Booking Modification and Cancellation

The project now includes:

- UC-06 Modify Confirmed Booking
- UC-07 Cancel Confirmed Booking

Only `CONFIRMED` bookings can be modified or cancelled. Pending and cancelled bookings are not handled by these flows.

Booking modification changes the booking slot to another available slot for the same field. No additional payment for price differences is implemented.

Booking cancellation uses the facility `CancellationPolicy`. If cancellation is allowed, the booking is marked `CANCELLED`. Refunds are mock refunds recorded through `Payment` with payment type `REFUND`; no real external refund integration exists.

Tests and UI polishing will be implemented in later steps.
