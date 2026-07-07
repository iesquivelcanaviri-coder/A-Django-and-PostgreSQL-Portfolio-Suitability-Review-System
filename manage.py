#!/usr/bin/env python
# DJANGO COMMAND-LINE ENTRY POINT
# This file is called manage.py and is created automatically
# when a new Django project is created.

# It acts as the main command-line entry point for the project.
# Commands such as the following all use this file:

# python manage.py runserver
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser
# python manage.py test

# In simple terms, manage.py tells Django which project settings
# to use and then passes the command entered in the terminal to
# Django's command-line system.

# ------------------------------------------------------------
# IMPORT STANDARD PYTHON MODULES
# ------------------------------------------------------------
# The os module is used to work with operating-system features.
# In this file, it is used to set the Django settings module.
import os

# The sys module gives access to command-line arguments.
# For example, when the user runs:
# python manage.py runserver
# sys.argv stores the command and its arguments so Django can
# understand which administrative task should be performed.
import sys

# ============================================================
# MAIN FUNCTION
# ============================================================
def main():
    """ Run Django administrative commands.
    This function connects the manage.py command-line file to
    the SuitabilityDesk Django project.
    
    It performs three main tasks:
    1. It tells Django where the project settings are located.
    2. It imports Django's command-line command processor.
    3. It sends the terminal command to Django for execution."""

    # --------------------------------------------------------
    # SET THE DJANGO SETTINGS MODULE
    # --------------------------------------------------------
    # Django needs to know which settings.py file belongs to this project.
    # 'suitabilitydesk.settings' means:
    # suitabilitydesk/
    #     settings.py
    
    # setdefault() only creates this environment variable if it
    # has not already been set somewhere else.
    
    # This allows another environment, such as testing or
    # production, to provide a different settings module when required.
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "suitabilitydesk.settings",
    )

    # --------------------------------------------------------
    # IMPORT DJANGO'S COMMAND-LINE PROCESSOR
    # --------------------------------------------------------
    try:
        # execute_from_command_line() reads the command entered
        # after manage.py and runs the matching Django task.
        # Examples:
        # runserver       -> starts the development server
        # makemigrations  -> prepares database schema changes
        # migrate         -> applies migrations to the database
        # createsuperuser -> creates an administrator account
        # test            -> runs automated tests
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        # This error usually means that:
        #
        # - Django has not been installed
        # - the virtual environment is not activated
        # - the wrong Python interpreter is being used
        # - the Python path is incorrectly configured
        #
        # "from exc" keeps the original error information,
        # making the problem easier to diagnose.
        raise ImportError(
            "Could not import Django. Check that Django is installed, "
            "the virtual environment is activated, and the correct "
            "Python interpreter is being used."
        ) from exc

    # --------------------------------------------------------
    # EXECUTE THE REQUESTED DJANGO COMMAND
    # --------------------------------------------------------
    # sys.argv contains the full command entered in the terminal.
    # For example:
    # ["manage.py", "runserver"]
    # Django reads these values and performs the requested task.
    execute_from_command_line(sys.argv)


# ============================================================
# RUN THE MAIN FUNCTION
# ============================================================
# Python automatically gives the special value "__main__" to
# __name__ when this file is executed directly.
# Therefore, when the user runs:
# python manage.py runserver
# the condition below is True and main() is called.
# If this file is imported into another Python file, main() will
# not run automatically.
if __name__ == "__main__":
    main()