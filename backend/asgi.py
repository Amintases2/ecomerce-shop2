"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_asgi_application()

# import os
# import sys
#
# try:
#     sys.path.remove('/usr/lib/python3/dist-packages')
# except:
#     pass
#
# sys.path.append('/home/c/cy45879/django/public_html/mysite/')
# sys.path.append('/home/c/cy45879/django/venv/lib/python3.6/site-packages/')
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timewebtest.settings')
#
# from django.core.wsgi import get_wsgi_application
#
# application = get_wsgi_application()
