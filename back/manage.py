#!/usr/bin/env pyton
"""Django's command-line utility for administrative tasks."""
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and"
            "available on your PYTHONPATH enviroment variable? Did you"
            "forget to activate virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
