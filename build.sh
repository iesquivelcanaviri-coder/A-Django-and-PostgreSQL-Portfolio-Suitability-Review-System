#!/usr/bin/env bash
# ============================================================
# SUITABILITYDESK - RENDER DEPLOYMENT BUILD SCRIPT
# File: build.sh
# Purpose:
# This shell script prepares the Django application for
# deployment on Render.
# Render runs this file during the build stage, before the
# Gunicorn production server starts the Django application.

# The script performs three main deployment tasks:
# 1. Installs the Python packages listed in requirements.txt.
# 2. Applies Django migrations to the PostgreSQL database.
# 3. Collects CSS, JavaScript and image files for production.
# If one of these commands fails, the build stops immediately.
# This prevents Render from deploying an incomplete or broken
# version of the application.
# This file is used by setting the Render build command to:
# ./build.sh
# ============================================================

# ------------------------------------------------------------
# Stop the build when a command fails
# ------------------------------------------------------------
# set -o errexit tells the shell to stop running this script
# immediately when any command returns an error.
# Without this setting, the script could continue after a failed
# installation, migration or static-file collection command.
# Render might then attempt to start an application that is not
# correctly prepared.
# For example:
# - If pip cannot install a required package, the build stops.
# - If a database migration fails, the build stops.
# - If collectstatic fails, the build stops.
# "set -e" is a shorter version of the same command.
set -o errexit

# ------------------------------------------------------------
# # 1. INSTALL THE PYTHON DEPENDENCIES 
#Read and install packages from requirements.txt
# ------------------------------------------------------------
# pip is Python's package installer.
# The -r option tells pip to read the package names and versions
# from the requirements.txt file.
# requirements.txt contains the external libraries required by
# the project, for example:
# - Django:
#   Provides the web framework, ORM, templates, authentication
#   system and other core application functionality.
# - psycopg:
#   Allows Django to connect to the PostgreSQL database.
# - Gunicorn:
#   Runs the Django application as a production WSGI server.
# - WhiteNoise:
#   Allows the deployed application to serve collected static
#   files such as CSS and JavaScript.
# Render creates a clean deployment environment for each build.
# Therefore, these packages must be installed before Django commands or the production server can run.
pip install -r requirements.txt

# ------------------------------------------------------------
# 2. APPLY THE DATABASE MIGRATIONS
# Synchronise Django models with PostgreSQL
# ------------------------------------------------------------
# Django models are Python classes that describe the structure
# of the application's database tables.
# For example, the project may contain models representing:
# - user profiles
# - portfolio review projects
# - suitability assessments
# - stakeholders
# - categories
# - messages
# - audit records
# Migration files describe how the database schema should change
# when a model is created or modified.
# The migrate command applies all migration files that have not
# already been applied to the connected database.
# In production, Django connects to PostgreSQL using the
# DATABASE_URL environment variable configured in Render.
#
# This command can:
# - create missing tables
# - add new columns
# - change field properties
# - create indexes
# - create foreign-key relationships
# - add constraints
# Django records completed migrations in the django_migrations
# table. Therefore, migrations that have already been applied
# are not repeated unnecessarily.
# Running migrations during deployment ensures that the database
# structure matches the version of the application being deployed.
python manage.py migrate


# ------------------------------------------------------------
# 3. COLLECT THE PRODUCTION STATIC FILES
# Gather CSS, JavaScript and images into STATIC_ROOT
# ------------------------------------------------------------
# Static files are files used by the browser that are not created
# dynamically by Django.
# Examples include:
# - static/css/style.css
# - static/js/script.js
# - logos and interface images
# During local development, Django can locate static files across
# the project's static directories.
#
# In production, these files need to be gathered into one final
# directory defined by STATIC_ROOT in settings.py.
# The collectstatic command searches the installed applications
# and project static directories, then copies the files into
# STATIC_ROOT.

# WhiteNoise can then serve those collected files efficiently
# when the Django application is deployed.
#
# The --noinput option prevents Django from asking questions in
# the terminal. This is necessary because Render builds are
# automated and cannot respond to interactive prompts.
python manage.py collectstatic --noinput


# ============================================================
# BUILD SCRIPT COMPLETED
# ============================================================
#
# If the script reaches this point, the required dependencies
# were installed, the PostgreSQL migrations were applied and the
# static files were collected successfully.
#
# Render can now start the production application using Gunicorn.
#
# Example Render start command:
#
# gunicorn config.wsgi:application
#
# ============================================================