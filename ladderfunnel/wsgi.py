"""
WSGI config for ladderfunnel project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.exceptions import ImproperlyConfigured
from pathlib import Path

def check_database_exists():
    BASE_DIR = Path(__file__).resolve().parent.parent
    db_path = os.path.join(BASE_DIR,'db.sqlite3')  # Ensure this path is correct
    if not os.path.isfile(db_path):
        raise ImproperlyConfigured(f"Database file {db_path} does not exist.")

# Use this function as part of your application startup routine:
check_database_exists()


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ladderfunnel.settings')

application = get_wsgi_application()
