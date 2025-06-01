"""
URLs do app Itens - Sistema de Achados & Perdidos UFT Palmas
"""

from django.urls import path
from itens.views import (
    # Views principais para achados e perdidos
    ListarItens, DetalheItem, CriarItem, EditarItem, DeletarItem,
    adicionar_comentario, reivindicar_item, agendar_encontro, 
    marcar_como_resolvido, meus_itens, minhas_reivindicacoes, 
    reivindicacoes_recebidas, aprovar_reivindicacao, rejeitar_reivindicacao,
    itens_recentes_api,
    # Views de compatibilidade (legado)
    ListarAnuncios, CriarAnuncios, DeletarAnuncio, EditarAnuncios
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
    path('<int:item_id>/reivindicar/', reivindicar_item, name='reivindicar-item'),
    path('<int:item_id>/agendar-encontro/', agendar_encontro, name='agendar-encontro'),
    path('<int:item_id>/marcar-resolvido/', marcar_como_resolvido, name='marcar-resolvido'),
    
    # Páginas do usuário
    path('meus-itens/', meus_itens, name='meus-itens'),
    path('minhas-reivindicacoes/', minhas_reivindicacoes, name='minhas-reivindicacoes'),
    path('reivindicacoes-recebidas/', reivindicacoes_recebidas, name='reivindicacoes-recebidas'),
    
    # Gerenciamento de reivindicações
    path('reivindicacao/<int:pk>/aprovar/', aprovar_reivindicacao, name='aprovar-reivindicacao'),
    path('reivindicacao/<int:pk>/rejeitar/', rejeitar_reivindicacao, name='rejeitar-reivindicacao'),
    
    # API endpoints
    path('api/recentes/', itens_recentes_api, name='itens-recentes-api'),
    
    # URLs de compatibilidade (legado - serão removidas)
    path('anuncios/', ListarAnuncios.as_view(), name='listar-anuncios'),
    path('anuncios/novo/', CriarAnuncios.as_view(), name='criar-anuncio'),
    path('anuncios/<int:pk>/editar/', EditarAnuncios.as_view(), name='editar-anuncio'),
    path('anuncios/<int:pk>/deletar/', DeletarAnuncio.as_view(), name='deletar-anuncio'),
]