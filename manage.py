"""None of the code is this manage.py file is mine, it is automatically generated
by Django when I ran 'django-admin startproject Peerspace' in the commandline.

The code in this file is the entry point to the project, it lets me run vital
commands from the commandline.
"""

#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Peerspace.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
