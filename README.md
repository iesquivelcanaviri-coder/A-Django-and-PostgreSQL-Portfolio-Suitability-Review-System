# SuitabilityDesk  
## A Django and PostgreSQL Portfolio Suitability Review System

---

## Student Details

**Student Name:** Irene Esquivel Canaviri  
**Module:** Frameworks  
**Assignment:** Building a Web Application with Django and a Database  

---

# 1. Project Overview

SuitabilityDesk is an educational Django web application connected to a PostgreSQL database. The project simulates a realistic and lawful portfolio-management support workflow where users can record client information, complete financial and risk profiles, create investment mandates, categorise holdings, manage portfolio review projects, communicate through an internal inbox and preserve an evidence trail.

The application is intentionally **not** a trading platform and does **not** provide regulated investment advice. Instead, it focuses on the governance process behind portfolio management:

```text
Know the client
        ↓
Assess suitability
        ↓
Define the investment mandate
        ↓
Categorise holdings
        ↓
Open a portfolio review project
        ↓
Approve, reject or request more information
        ↓
Preserve messages and audit evidence
````

This makes the project suitable for the Frameworks assignment while also supporting a realistic understanding of how portfolio-management workflows operate in practice.

---

# 2. Live Deployment

## Render Deployment URL

```text
https://a-django-and-postgresql-portfolio.onrender.com
```

---

# 3. GitHub Repository

```text
https://github.com/iesquivelcanaviri-coder/A-Django-and-PostgreSQL-Portfolio-Suitability-Review-System.git
```

---

# 4. Assignment Requirement Coverage

| Assignment Requirement                    | How SuitabilityDesk Covers It                                                                                     |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Django backend framework                  | Uses a full Django project with modular apps: `accounts`, `clients`, `mandates`, `messaging` and `dashboard`.     |
| PostgreSQL database                       | Uses PostgreSQL through `DATABASE_URL`, `dj-database-url` and Neon/Render-compatible configuration.               |
| HTML, CSS and JavaScript                  | Uses Django templates, Bootstrap 5, custom CSS and JavaScript.                                                    |
| User registration and login               | Includes user registration, login, logout and Django authentication templates.                                    |
| Users can update personal/contact details | Users can update name, email, phone, organisation and job title.                                                  |
| Email-based password recovery             | Uses Django's built-in password reset workflow and templates.                                                     |
| Project data storage                      | `PortfolioReviewProject` stores project name, description, start date, end date, status and stakeholders.         |
| Inbox functionality                       | Users can compose, receive, read, send and archive messages.                                                      |
| Store and categorise data                 | Holdings are categorised by `AssetCategory`; mandates include status, ESG preference and restrictions.            |
| Bootstrap responsive layout               | Base template uses Bootstrap navbar, cards, forms, tables, badges and responsive grid layouts.                    |
| JavaScript interactivity                  | Includes real-time form validation, allocation warnings and auto-closing alerts.                                  |
| Password security                         | Uses Django's built-in password hashing system.                                                                   |
| User roles and permissions                | Uses roles such as Client, Adviser, Portfolio Manager, Compliance Reviewer and Admin.                             |
| Modular extension capability              | Separate apps make future API, reporting, analytics or finance extensions easier.                                 |
| Hosted web app evidence                   | Project includes Render-ready files: `Procfile`, `runtime.txt`, `requirements.txt`, `build.sh` and `render.yaml`. |
| README and comments                       | README explains the project, setup, database connection, testing and deployment process.                          |

---

# 5. Portfolio Management Workflow

The project is designed around a realistic suitability-review process.

```text
User registers or logs in
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

This workflow demonstrates both Django functionality and portfolio-management concepts.

---

# 6. Main Django Apps and File Connections

## `suitabilitydesk/`

This is the main Django project configuration folder.

| File          | Purpose                                                                                              |
| ------------- | ---------------------------------------------------------------------------------------------------- |
| `settings.py` | Stores project settings, installed apps, database configuration, static files and security settings. |
| `urls.py`     | Connects project-level routes to app-level URL files.                                                |
| `wsgi.py`     | Used by Gunicorn when the project is deployed on Render.                                             |
| `asgi.py`     | Standard Django ASGI entry point for asynchronous deployment support.                                |

The `settings.py` file reads the PostgreSQL connection from the `DATABASE_URL` environment variable. This allows the project to use Neon PostgreSQL locally and on Render without hardcoding private database credentials.

---

## `accounts/`

The `accounts` app manages user identity, authentication-related profile information and role-based access.

Main responsibilities:

* user profile extension
* contact details
* role storage
* permission checks
* personal information updates

Important model:

| Model         | Purpose                                                                            |
| ------------- | ---------------------------------------------------------------------------------- |
| `UserProfile` | Extends Django's built-in user model with role, phone, organisation and job title. |

Roles used in the project:

```text
Client
Adviser
Portfolio Manager
Compliance Reviewer
Admin
```

These roles are used to restrict sensitive actions such as mandate approval.

---

## `clients/`

The `clients` app stores client suitability information.

Main responsibilities:

* client identity records
* financial profile records
* risk and suitability assessment records

Important models:

| Model              | Purpose                                                                            |
| ------------------ | ---------------------------------------------------------------------------------- |
| `ClientProfile`    | Stores client identity and contact information.                                    |
| `FinancialProfile` | Stores income, net worth, liquidity needs, liabilities and investment experience.  |
| `RiskAssessment`   | Stores risk tolerance, risk capacity and a simple educational suitability outcome. |

This app supports the “know your client” and suitability-assessment part of the portfolio-management workflow.

---

## `mandates/`

The `mandates` app stores the core portfolio-management workflow.

Main responsibilities:

* investment mandates
* asset categories
* holdings
* portfolio review projects
* stakeholders
* approvals
* audit logs

Important models:

| Model                    | Purpose                                                                                                               |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| `InvestmentMandate`      | Stores objective, benchmark, base currency, ESG preference, restrictions, status and approval data.                   |
| `AssetCategory`          | Stores asset categories such as equities, bonds, ETFs or cash.                                                        |
| `PortfolioHolding`       | Stores holdings linked to an investment mandate.                                                                      |
| `PortfolioReviewProject` | Stores the project name, description, start date, end date, stakeholders and status required by the assignment brief. |
| `Stakeholder`            | Links users to review projects with a defined stakeholder role.                                                       |
| `AuditLog`               | Stores governance actions such as creation, update, approval or rejection.                                            |

This app provides the strongest evidence of database integration, relationships and CRUD logic.

---

## `messaging/`

The `messaging` app implements the required inbox functionality.

Main responsibilities:

* compose messages
* receive messages
* read messages
* send messages
* archive messages
* link messages to portfolio review projects

Important model:

| Model     | Purpose                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------- |
| `Message` | Stores sender, recipient, subject, body, related project, sent time, read status and archive status. |

This app satisfies the assignment requirement for inbox functionality where users can send, receive and archive messages.

---

## `dashboard/`

The `dashboard` app provides the landing page and authenticated dashboard.

Main responsibilities:

* public home page
* authenticated dashboard
* summary cards
* recent records
* portfolio-review overview

The dashboard displays information such as:

* client count
* mandate count
* open project count
* unread messages
* recent review projects
* suitability assessments
* holdings summary

---

# 7. Database Schema Summary

## Core Database Tables

| Table                             | Purpose                                                                     |
| --------------------------------- | --------------------------------------------------------------------------- |
| `auth_user`                       | Built-in Django user table. Stores usernames, emails and password hashes.   |
| `accounts_userprofile`            | Stores user roles and contact details.                                      |
| `clients_clientprofile`           | Stores client identity and contact information.                             |
| `clients_financialprofile`        | Stores financial background and liquidity context.                          |
| `clients_riskassessment`          | Stores risk tolerance, risk capacity and suitability outcome.               |
| `mandates_investmentmandate`      | Stores investment mandate details and approval status.                      |
| `mandates_assetcategory`          | Stores holding categories such as equities, bonds, ETFs or cash.            |
| `mandates_portfolioholding`       | Stores categorised holdings linked to mandates.                             |
| `mandates_portfolioreviewproject` | Stores project name, description, start/end dates, stakeholders and status. |
| `mandates_stakeholder`            | Links users to review projects.                                             |
| `messaging_message`               | Stores inbox, sent and archived messages.                                   |
| `mandates_auditlog`               | Stores governance evidence for important actions.                           |

---

# 8. Database Relationship Summary

The project demonstrates relational database design through Django's ORM.

```text
User
 └── UserProfile

ClientProfile
 ├── FinancialProfile
 ├── RiskAssessment
 └── InvestmentMandate

InvestmentMandate
 ├── PortfolioHolding
 └── PortfolioReviewProject

PortfolioReviewProject
 ├── Stakeholder
 ├── Message
 └── AuditLog

AssetCategory
 └── PortfolioHolding
```

Examples of database concepts demonstrated:

* primary keys
* foreign keys
* one-to-one relationships
* one-to-many relationships
* many-to-many style stakeholder relationships
* model choices
* timestamps
* status fields
* role-based access
* database-backed messages
* database-backed categorisation

---

# 9. CRUD Evidence

| CRUD Operation   | Example in Project                                                                                             |
| ---------------- | -------------------------------------------------------------------------------------------------------------- |
| Create           | Create users, clients, financial profiles, risk assessments, mandates, holdings, review projects and messages. |
| Read             | Dashboard, client lists, mandate lists, project details and inbox pages read from PostgreSQL.                  |
| Update           | Update user profile, client profile, financial profile, risk assessment, mandates and project statuses.        |
| Delete / Archive | Delete or archive records such as holdings, messages and review items where appropriate.                       |

The project demonstrates CRUD through both function-based and class-based Django views.

---

# 10. Authentication and Authorization

The project uses Django's built-in authentication system.

Implemented authentication features:

* registration
* login
* logout
* profile update
* password reset request
* password reset confirmation
* password reset completion

Authorization features:

* private pages require login
* mandate approval is restricted by user role
* users can only access relevant project or message data
* administrative control remains available through Django admin

Important security note:

> Passwords are not stored in plain text. Django stores passwords using secure salted hashing through its built-in authentication framework.

---

# 11. Frontend Design

The project uses Django templates with Bootstrap 5 and custom CSS.

Frontend features include:

* responsive navigation bar
* reusable `base.html`
* Bootstrap cards
* Bootstrap tables
* Bootstrap badges
* Bootstrap alerts
* dashboard summary panels
* forms with clear labels
* mobile-friendly page layout

Static files are stored in:

```text
static/
├── css/
│   └── style.css
├── js/
│   └── script.js
└── images/
```

---

# 12. JavaScript Functionality

JavaScript is used to make the interface more interactive.

Examples:

* real-time date validation
* allocation warning when portfolio weights exceed limits
* auto-closing success and error alerts
* collapsible dashboard sections
* form feedback before submission

JavaScript supports usability, but important validation is also handled server-side in Django.

---

# 13. Local Installation and Neon PostgreSQL Setup

## 13.1 Clone the Repository

```bash
git clone https://github.com/iesquivelcanaviri-coder/A-Django-and-PostgreSQL-Portfolio-Suitability-Review-System.git
cd A-Django-and-PostgreSQL-Portfolio-Suitability-Review-System
```

---

## 13.2 Open the Project in VS Code

Open the project folder in VS Code.

The folder should contain:

```text
manage.py
requirements.txt
README.md
Procfile
runtime.txt
.gitignore
```

Make sure the terminal is inside the same folder as `manage.py`.

---

        ## 13.3 Create a Virtual Environment

        ```bash
        python3 -m venv .venv
        ```

        ---

        ## 13.4 Activate the Virtual Environment

        ```bash
        source .venv/bin/activate
        ```

        When activated, the terminal should show:

        ```text
        (.venv)
        ```

        If Anaconda is also active, you may see:

        ```text
        (.venv) (base)
        ```

        This is acceptable as long as `(.venv)` appears.

        ---

        ## 13.5 Install Requirements

        ```bash
        pip install -r requirements.txt
        ```

        ## Create the .env file again
        Inside .env, add:
        SECRET_KEY=replace-this-with-a-long-random-secret-key
        DEBUG=True
        DATABASE_URL=postgresql://PASTE-YOUR-NEON-CONNECTION-STRING-HERE
        ALLOWED_HOSTS=127.0.0.1,localhost
        EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
        DEFAULT_FROM_EMAIL=noreply@example.com

        ## Run Django checks
        Run: python manage.py check

        ## Run migrations
        Run: python manage.py makemigrations
        then: python manage.py migrate

                ## Create a superuser
                Run: python manage.py createsuperuser
                Django will ask for:
                        Username
                        Email address
                        Password
                        Password again
                If it says the username already exists, that means your Neon database already has users. Use a different username or log in with the existing on

        ##Run the server
        Run: python manage.py runserver

---

## 13.6 Create the Neon PostgreSQL Database

Go to:

```text
https://console.neon.tech
```

Create a new project using:

```text
Project name: suitabilitydesk_db
Postgres version: 18
Region: AWS Europe West 2 (London)
Neon Auth: OFF
```

Then click:

```text
Create project
```

---

## 13.7 Copy the Neon Connection String

Inside the Neon project dashboard:

```text
Connect → Connection string
```

Copy the connection string.

It should start with:

```text
postgresql://
```

It should include:

```text
sslmode=require
```

Do not share the connection string publicly because it contains the database password.

---

## 13.8 Create the `.env` File

In the same folder as `manage.py`, create a file called:

```text
.env
```

Add:

```env
SECRET_KEY=replace-this-with-a-long-random-secret-key
DEBUG=True
DATABASE_URL=postgresql://PASTE-YOUR-NEON-CONNECTION-STRING-HERE
ALLOWED_HOSTS=127.0.0.1,localhost
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@example.com
```

Replace:

```text
postgresql://PASTE-YOUR-NEON-CONNECTION-STRING-HERE
```

with the real Neon connection string.

---

## 13.9 Confirm `.gitignore`

Open `.gitignore` and make sure it includes:

```gitignore
.env
.venv/
venv/
__pycache__/
*.pyc
db.sqlite3
staticfiles/
media/
.DS_Store
```

The `.env` file must not be uploaded to GitHub.

---

## 13.10 Create Migrations

```bash
python manage.py makemigrations
```

---

## 13.11 Apply Migrations to Neon PostgreSQL

```bash
python manage.py migrate
```

If this works, Django has created the database tables inside Neon PostgreSQL.

---

## 13.12 Create the Admin User

```bash
python manage.py createsuperuser
```

Django will ask for:

```text
Username
Email address
Password
Password again
```

This user is used to access the Django admin panel.

---

## 13.13 Run the Local Development Server

```bash
python manage.py runserver
```

Open the website:

```text
http://127.0.0.1:8000/
```

Open the admin panel:

```text
http://127.0.0.1:8000/admin/
```
---
## 13.14 Correct Development and Deployment Order

The project should be built and deployed in this order:

```text
1. Build the Django project in VS Code
2. Create apps, models, views, templates, static files and forms
3. Test the project locally
4. Add .env to .gitignore
5. Push the safe project files to GitHub
6. Create the Neon PostgreSQL database
7. Copy the Neon DATABASE_URL
8. Add DATABASE_URL to the local .env file
9. Run migrations locally using Neon
10. Test the local website and admin panel again
11. Create the Render web service
12. Connect Render to GitHub
13. Add Render environment variables
14. Set Render build and start commands
15. Deploy the live website

In simple terms:

VS Code = build and test the code
GitHub = store the safe project files
Neon = store the PostgreSQL database
Render = host the live Django website

Correct workflow:

Build locally → Push to GitHub → Create Neon → Test Neon locally → Deploy with Render

Render is created last because it needs the GitHub code, the Neon database connection string and the Django environment variables.

---

## 14. Render Deployment Setup

This section explains how to deploy the Django project to Render after the project code has been pushed to GitHub and the Neon PostgreSQL database has been created.

Render is used to host the live Django web application. Neon is used to host the PostgreSQL database. GitHub stores the project code.

```text
GitHub = stores the Django code
Neon = stores the PostgreSQL database
Render = hosts the live web application
```

---

## 14.1 Before Starting Render

Before creating the Render web service, confirm that the project works locally.

Run:

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Then check:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/
```

If the local project works, push the latest safe version to GitHub:

```bash
git status
git add .
git commit -m "Prepare Django project for Render deployment"
git push origin main
```

Important: `.env` must not be uploaded to GitHub.

---

## 14.2 Create a Render Web Service

Go to:

```text
https://dashboard.render.com
```

Click:

```text
New + → Web Service
```

Connect the GitHub repository:

```text
A-Django-and-PostgreSQL-Portfolio-Suitability-Review-System
```

---

## 14.3 Render General Settings

Use the following settings:

```text
Name: A-Django-and-PostgreSQL-Portfolio-Suitability-Review-System
Language: Python 3
Branch: main
Region: Frankfurt (EU Central)
Instance Type: Free
Root Directory: leave empty
```

The root directory should stay empty because `manage.py` is in the main repository folder.

---

## 14.4 Render Build Command

In Render, set the Build Command to:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

This command does three things:

```text
1. Installs the Python packages from requirements.txt
2. Collects static files for production
3. Applies Django migrations to the Neon PostgreSQL database
```

---

## 14.5 Render Start Command

Set the Start Command to:

```bash
gunicorn suitabilitydesk.wsgi:application
```

This tells Render to start the Django application using Gunicorn.

The word before `.wsgi` must match the Django project folder that contains:

```text
settings.py
urls.py
wsgi.py
asgi.py
```

In this project, that folder is:

```text
suitabilitydesk
```

---

## 14.6 Render Health Check Path

Set the Health Check Path to:

```text
/
```

This allows Render to check whether the homepage is responding correctly.

---

# 15. Render Environment Variables

Render cannot access the local `.env` file from the developer's computer. Therefore, the production settings must be added manually in the Render Environment page.

Go to:

```text
Render Dashboard → Web Service → Environment
```

Click:

```text
Add Environment Variable
```

Add the following variables one by one.

---

## 15.1 `SECRET_KEY`

```text
Key: SECRET_KEY
Value: use a generated secret key from Render
```

This is Django's private security key. It must not be shared or committed to GitHub.

---

## 15.2 `DEBUG`

```text
Key: DEBUG
Value: False
```

`DEBUG` must be `False` in production so that Django does not show private technical error details on the live website.

---

## 15.3 `DATABASE_URL`

```text
Key: DATABASE_URL
Value: your Neon PostgreSQL connection string
```

The value should start with:

```text
postgresql://
```

Example format:

```text
postgresql://username:password@host/neondb?sslmode=require
```

This connects the live Render website to the Neon PostgreSQL database.

Do not include `DATABASE_URL=` inside the value box. Render already stores the key separately.

Correct:

```text
Key: DATABASE_URL
Value: postgresql://username:password@host/neondb?sslmode=require
```

Incorrect:

```text
Key: DATABASE_URL
Value: DATABASE_URL=postgresql://username:password@host/neondb?sslmode=require
```

---

## 15.4 `ALLOWED_HOSTS`

Use the Render domain without `https://`.

For this project, the Render domain is:

```text
a-django-and-postgresql-portfolio.onrender.com
```

Add:

```text
Key: ALLOWED_HOSTS
Value: a-django-and-postgresql-portfolio.onrender.com
```

---

## 15.5 `CSRF_TRUSTED_ORIGINS`

Use the Render domain with `https://`.

```text
Key: CSRF_TRUSTED_ORIGINS
Value: https://a-django-and-postgresql-portfolio.onrender.com
```

This allows Django forms to work correctly on the deployed Render website.

---

## 15.6 `EMAIL_BACKEND`

```text
Key: EMAIL_BACKEND
Value: django.core.mail.backends.console.EmailBackend
```

This means password reset emails are printed in the server logs instead of being sent through a real email service. This is suitable for development and academic demonstration.

---

## 15.7 `DEFAULT_FROM_EMAIL`

```text
Key: DEFAULT_FROM_EMAIL
Value: noreply@suitabilitydesk.com
```

This is the default sender address used by Django's password reset system.

---

## 15.8 Final Render Environment Variable Checklist

The final Render Environment page should contain:

```text
SECRET_KEY = generated secret key
DEBUG = False
DATABASE_URL = Neon PostgreSQL connection string
ALLOWED_HOSTS = a-django-and-postgresql-portfolio.onrender.com
CSRF_TRUSTED_ORIGINS = https://a-django-and-postgresql-portfolio.onrender.com
EMAIL_BACKEND = django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL = noreply@suitabilitydesk.com
```

---

# 16. Deploy the Web Service

After the settings and environment variables are added, click:

```text
Deploy Web Service
```

If the service already exists, use:

```text
Manual Deploy → Deploy latest commit
```

Render will then:

```text
1. Pull the latest code from GitHub
2. Install requirements
3. Collect static files
4. Run migrations
5. Start the Django application with Gunicorn
```

---

# 17. Check the Live Website

After deployment finishes, open the live Render URL:

```text
https://a-django-and-postgresql-portfolio.onrender.com
```

Check the following pages:

```text
/
admin/
accounts/login/
accounts/register/
dashboard/
```

The admin page should be:

```text
https://a-django-and-postgresql-portfolio.onrender.com/admin/
```

---

# 18. Create a Superuser on Render

If the local superuser does not exist on the live Neon database, create one from the Render Shell.

Go to:

```text
Render Dashboard → Web Service → Shell
```

Run:

```bash
python manage.py createsuperuser
```

Enter:

```text
Username
Email address
Password
Password again
```

Then log in at:

```text
https://a-django-and-postgresql-portfolio.onrender.com/admin/
```

---

# 19. Testing

Run:

```bash
python manage.py test
```

The test suite checks examples such as:

* public home page loads
* dashboard requires login
* logged-in dashboard loads
* risk assessment outcome is calculated
* client users cannot approve mandates
* private messages are protected
* core models save correctly

Additional deployment checks can be run with:

```bash
python manage.py check
python manage.py check --deploy
```

---

# 20. Common Render Errors and Fixes

## Error: `UnknownSchemeError: Scheme '://' is unknown`

This means `DATABASE_URL` is incorrect.

Fix:

```text
DATABASE_URL must start with postgresql://
```

Correct format:

```text
postgresql://username:password@host/neondb?sslmode=require
```

---

## Error: `DisallowedHost`

This means `ALLOWED_HOSTS` is incorrect.

Fix:

```text
ALLOWED_HOSTS = a-django-and-postgresql-portfolio.onrender.com
```

Do not include `https://`.

---

## Error: CSRF verification failed

This means `CSRF_TRUSTED_ORIGINS` is incorrect.

Fix:

```text
CSRF_TRUSTED_ORIGINS = https://a-django-and-postgresql-portfolio.onrender.com
```

This one must include `https://`.

---

## Error: Static files not loading

Check that the Build Command includes:

```bash
python manage.py collectstatic --noinput
```

Also check that `settings.py` includes the correct static files configuration.

---

## Error: Application failed to start

Check the Start Command:

```bash
gunicorn suitabilitydesk.wsgi:application
```

The word before `.wsgi` must match the folder that contains `wsgi.py`.

---

# 21. Security Notes

Security features included:

* Django password hashing
* CSRF protection on forms
* login-required views
* role-based mandate approval
* environment variables for secrets
* `.env` excluded from GitHub
* PostgreSQL credentials not hardcoded in source code
* object-level checks for private messages and approval actions
* `DEBUG=False` expected in production

---

# 22. Files Not Uploaded to GitHub

The following files and folders should not be committed:

```text
.env
.venv/
venv/
db.sqlite3
media/
staticfiles/
.DS_Store
```

These are excluded through `.gitignore`.

---

# 23. Useful Commands

## Activate Virtual Environment

```bash
source .venv/bin/activate
```

## Install Requirements

```bash
pip install -r requirements.txt
```

## Create Migrations

```bash
python manage.py makemigrations
```

## Apply Migrations

```bash
python manage.py migrate
```

## Create Admin User

```bash
python manage.py createsuperuser
```

## Run Local Server

```bash
python manage.py runserver
```

## Run Tests

```bash
python manage.py test
```

## Stop Local Server

```text
CONTROL + C
```

---

# 24. Academic and Financial Disclaimer

This project is for educational purposes only. It demonstrates Django, PostgreSQL, authentication, authorization, Bootstrap, JavaScript, testing and deployment concepts through a realistic portfolio suitability workflow.

It does not provide regulated investment advice, does not recommend financial products and does not execute trades.

---

# 25. Summary

SuitabilityDesk demonstrates the key Frameworks assignment requirements through a lawful and realistic finance-related web application. It combines Django, PostgreSQL, authentication, authorization, Bootstrap, JavaScript, CRUD operations, inbox functionality, categorised data, role-based approval and deployment readiness.

The application supports a professional portfolio suitability workflow while remaining appropriate for an educational software-development assignment.

```

After you paste this into GitHub, your README will properly include the **Render deployment process**, the **environment variables**, and the **common Render errors/fixes**.
```
