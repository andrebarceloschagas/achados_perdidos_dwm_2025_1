import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'achados_perdidos_uft.settings')

application = get_wsgi_application()
