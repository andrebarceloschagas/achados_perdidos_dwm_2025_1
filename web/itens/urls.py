"""
URLs do app Itens - Sistema de Achados & Perdidos UFT Palmas
"""

from django.urls import path
from itens.views import (
    # Views principais para achados e perdidos
    ListarItens, DetalheItem, CriarItem, EditarItem, DeletarItem,
    adicionar_comentario, marcar_como_resolvido, meus_itens,
    itens_recentes_api
)

app_name = 'itens'

urlpatterns = [
    # URLs principais do sistema de achados e perdidos
    path('', ListarItens.as_view(), name='listar-itens'),
    path('<int:pk>/', DetalheItem.as_view(), name='detalhe-item'),
    path('novo/', CriarItem.as_view(), name='criar-item'),
    path('<int:pk>/editar/', EditarItem.as_view(), name='editar-item'),
    path('<int:pk>/deletar/', DeletarItem.as_view(), name='deletar-item'),
    
    # Ações específicas em itens
    path('<int:item_id>/comentario/', adicionar_comentario, name='adicionar-comentario'),
    path('<int:item_id>/marcar-resolvido/', marcar_como_resolvido, name='marcar-resolvido'),
    
    # Páginas do usuário
    path('meus-itens/', meus_itens, name='meus-itens'),
    
    # API endpoints
    path('api/recentes/', itens_recentes_api, name='itens-recentes-api'),
]
