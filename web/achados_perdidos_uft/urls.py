"""
URLs principais do Sistema de Achados & Perdidos
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from achados_perdidos_uft.views import PaginaInicial, LoginView, LogoutView, SobreView, RegistroView

# Configurações do painel administrativo
admin.site.site_header = "Achados & Perdidos - UFT Palmas"
admin.site.site_title = "Sistema UFT"
admin.site.index_title = "Painel Administrativo - Achados & Perdidos"

urlpatterns = [
    # Administração
    path('admin/', admin.site.urls),
    
    # Páginas principais
    path('', PaginaInicial.as_view(), name='pagina-inicial'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('sobre/', SobreView.as_view(), name='sobre'),
    
    # App de itens (achados e perdidos)
    path('itens/', include('itens.urls')),
    
    # API REST
    path('api/', include('itens.api_urls')),
]

# Servir arquivos de media em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
