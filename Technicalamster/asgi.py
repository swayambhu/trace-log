"""
ASGI config for Technicalamster project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Technicalamster.settings')

application = get_asgi_application()


def add_logs_to_excel():
    import openpyxl
    from openpyxl.styles import Font
    from openpyxl.styles import Alignment
    from openpyxl.styles import PatternFill
    from openpyxl.styles import Border, Side
    from openpyxl.utils import get_column_letters

