"""
URLs para a API REST do sistema de Achados & Perdidos
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from itens.api_views import (
    UserViewSet, ItemViewSet, ComentarioViewSet, ContatoItemViewSet
)
from itens.views_api import categorias_list, blocos_list
from achados_perdidos_uft.auth_views import (
    CustomTokenObtainPairView, LogoutView, 
    revoke_token, revoke_all_tokens
)

# Cria um router para as viewsets da API
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'itens', ItemViewSet)
router.register(r'comentarios', ComentarioViewSet)
router.register(r'contatos', ContatoItemViewSet)

# URLs da API
urlpatterns = [
    # Rotas de autenticação JWT
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Gerenciamento de tokens
    path('token/revoke/<int:token_id>/', revoke_token, name='revoke_token'),
    path('token/revoke-all/', revoke_all_tokens, name='revoke_all_tokens'),
    
    # Endpoints para categorias e blocos
    path('categorias/', categorias_list, name='categorias-list'),
    path('blocos/', blocos_list, name='blocos-list'),
    
    # Rotas de API baseadas em viewsets
    path('', include(router.urls)),
    
    # Opcionalmente incluir as URLs de autenticação do navegador DRF
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
