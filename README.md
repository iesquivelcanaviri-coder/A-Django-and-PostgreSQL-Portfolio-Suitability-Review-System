# SuitabilityDesk: A Django and PostgreSQL Portfolio Suitability Review System

## Student Details

**Student Name:** Irene Esquivel Canaviri  
**Module:** Frameworks  
**Assignment:** Building a Web Application with Django and a Database

---

# Project Overview

SuitabilityDesk is an educational Django web application connected to a PostgreSQL database. The project simulates a lawful and realistic portfolio-management support workflow where users record client details, complete risk/suitability assessments, create investment mandates, categorise holdings, manage portfolio review projects and communicate through an internal inbox.

The application is intentionally not a trading platform and does not provide regulated investment advice. It focuses on the portfolio-management process: know the client, assess suitability, define the mandate, review holdings, approve or reject the mandate, and keep an evidence trail.

---

# Assignment Requirement Coverage

| Assignment Requirement | How This Project Covers It |
| --- | --- |
| Django backend framework | Uses a full Django project with modular apps: accounts, clients, mandates, messaging and dashboard. |
| PostgreSQL database | Uses `DATABASE_URL` with `dj-database-url`, compatible with Neon/Render PostgreSQL. |
| User registration and login | Includes registration, login, logout and Django authentication templates. |
| Profile update | Users can update name, email, phone, organisation and job title. |
| Email password recovery | Uses Django's built-in password reset views and templates. |
| Project data storage | `PortfolioReviewProject` stores project name, description, start date, end date, status and stakeholders. |
| Inbox functionality | Users can compose, receive, read, send and archive messages. |
| Store and categorise data | Holdings are categorised by `AssetCategory`; mandates have statuses, ESG rules and restrictions. |
| Bootstrap responsive UI | Base template uses Bootstrap 5 responsive navbar, cards, forms, tables and badges. |
| JavaScript interactivity | Includes form validation, allocation warning and auto-closing alerts. |
| Security | Uses Django password hashing, CSRF protection, login-required views, role-based mandate approval and environment variables. |
| Modular extension | Separate apps and models make future API, reporting or finance extensions easier. |
| Deployment | Includes `requirements.txt`, `Procfile`, `runtime.txt`, `build.sh`, `render.yaml` and static file setup. |

---

# Portfolio Management Workflow

```text
User registers / logs in
        ↓
User updates personal and contact profile
        ↓
Adviser creates client profile
        ↓
Adviser records financial profile and risk assessment
        ↓
Adviser creates investment mandate
        ↓
Holdings are categorised by asset class
        ↓
Portfolio review project is opened with dates, status and stakeholders
        ↓
Portfolio manager or compliance reviewer approves the mandate
        ↓
Messages and audit logs preserve the evidence trail
```

---

# Main Apps and File Connections

## `suitabilitydesk/`

The main Django project folder. It contains `settings.py`, `urls.py`, `wsgi.py` and `asgi.py`.

* `settings.py` connects Django to PostgreSQL through `DATABASE_URL`.
* `urls.py` connects the project-level routes to the individual app URLs.
* `wsgi.py` is used by Gunicorn on Render.

## `accounts/`

Handles user registration, profile updates and role data.

* `UserProfile` extends Django's built-in user model with a role and contact details.
* Roles include Client, Adviser, Portfolio Manager, Compliance Reviewer and Admin.
* The role is used to restrict approval of investment mandates.

## `clients/`

Stores client and suitability data.

* `ClientProfile` stores identity and contact records.
* `FinancialProfile` stores net worth, liquidity needs, liabilities and investment experience.
* `RiskAssessment` calculates a simple educational suitability outcome.

## `mandates/`

Stores the portfolio-management workflow.

* `InvestmentMandate` stores objective, benchmark, currency, ESG preference, product restriction, status and approval data.
* `AssetCategory` categorises holdings.
* `PortfolioHolding` stores holdings linked to a mandate.
* `PortfolioReviewProject` stores project details required by the brief.
* `Stakeholder` links users to review projects.
* `AuditLog` stores governance actions.

## `messaging/`

Implements inbox functionality.

* Users can compose messages.
* Messages can be read, sent and archived.
* Messages can be connected to a portfolio review project.

## `dashboard/`

Provides the public home page and authenticated dashboard.

* Shows client count, mandate count, open project count and unread messages.
* Displays recent review projects, suitability assessments and holdings.

---

# Database Schema Summary

## Core Tables

| Table | Purpose |
| --- | --- |
| `auth_user` | Built-in Django users and password hashes. |
| `accounts_userprofile` | User role and contact information. |
| `clients_clientprofile` | Client identity and contact information. |
| `clients_financialprofile` | Financial background and liquidity context. |
| `clients_riskassessment` | Risk tolerance, risk capacity and suitability outcome. |
| `mandates_investmentmandate` | Investment mandate and approval status. |
| `mandates_assetcategory` | Holding categories such as equities or bonds. |
| `mandates_portfolioholding` | Categorised holdings linked to mandates. |
| `mandates_portfolioreviewproject` | Project name, description, dates, stakeholders and status. |
| `mandates_stakeholder` | User roles within a review project. |
| `messaging_message` | Inbox, sent and archived messages. |
| `mandates_auditlog` | Governance record of key actions. |

---

# CRUD Evidence

| CRUD Operation | Example in Project |
| --- | --- |
| Create | Create clients, financial profiles, risk assessments, mandates, holdings, projects and messages. |
| Read | Dashboard, client list, mandate list, project list and inbox read from the database. |
| Update | Update user profile, client profile, financial profile and mandates. |
| Delete / Archive | Delete holdings and archive messages. |

---

# Local Installation

## 1. Clone the repository

```bash
git clone https://github.com/iesquivelcanaviri-coder/A-Django-and-PostgreSQL-Portfolio-Suitability-Review-System.git
cd A-Django-and-PostgreSQL-Portfolio-Suitability-Review-System
```

## 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create a `.env` file based on `.env.example`.

For local SQLite testing, this is enough:

```text
SECRET_KEY=replace-with-secure-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

For PostgreSQL:

```text
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```

## 5. Run migrations

```bash
python manage.py migrate
```

## 6. Create a superuser

```bash
python manage.py createsuperuser
```

## 7. Optional: seed demo data

```bash
python manage.py seed_demo
```

Demo login accounts created by the seed command:

```text
username: adviser
password: ChangeMe123!

username: manager
password: ChangeMe123!
```

## 8. Run the application

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# Testing

Run:

```bash
python manage.py test
```

The tests check:

* public home page loads
* dashboard requires login
* logged-in dashboard loads
* risk assessment outcome is calculated
* client users cannot approve mandates

---

# Render Deployment

The project includes Render-ready files:

* `Procfile`
* `runtime.txt`
* `requirements.txt`
* `build.sh`
* `render.yaml`

## Render Build Command

```bash
./build.sh
```

## Render Start Command

```bash
gunicorn suitabilitydesk.wsgi:application
```

## Required Environment Variables

```text
SECRET_KEY=<secure generated secret>
DEBUG=False
DATABASE_URL=<Render or Neon PostgreSQL connection string>
ALLOWED_HOSTS=<your-render-domain>.onrender.com
CSRF_TRUSTED_ORIGINS=https://<your-render-domain>.onrender.com
```

---

# Security Notes

* Passwords are handled by Django's built-in authentication system.
* Passwords are not stored in plain text.
* CSRF protection is enabled on forms.
* Views that handle private data require login.
* Mandate approval is restricted by role.
* Environment variables are used for sensitive settings.
* The `.env` file is excluded from GitHub.

---

# Academic Note

This project is for educational purposes only. It demonstrates Django, PostgreSQL, authentication, authorization, Bootstrap, JavaScript and deployment concepts through a realistic portfolio suitability workflow. It does not provide regulated investment advice or execute trades.
