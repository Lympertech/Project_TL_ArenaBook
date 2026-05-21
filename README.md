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

5. Run migrations later, after verifying the skeleton and before using Django's database-backed features:

```powershell
python manage.py check
```

```powershell
python manage.py migrate
```

6. Run the development server:

```powershell
python manage.py runserver
```

Database models, forms, tests, authentication behavior, booking logic, payment logic, approval logic, and availability or conflict logic will be implemented in later steps after this project skeleton is verified.
