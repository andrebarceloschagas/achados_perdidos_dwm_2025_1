import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'achados_perdidos_uft.settings')

application = get_asgi_application()
