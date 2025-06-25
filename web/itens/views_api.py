"""
Views adicionais para a API REST
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import CATEGORIA_CHOICES, BLOCO_CHOICES

@api_view(['GET'])
@permission_classes([AllowAny])  # Permite acesso sem autenticação
def categorias_list(request):
    """
    API endpoint para listar todas as categorias disponíveis
    """
    categorias = [{'id': id, 'nome': nome} for id, nome in CATEGORIA_CHOICES]
    return Response(categorias)

@api_view(['GET'])
@permission_classes([AllowAny])  # Permite acesso sem autenticação
def blocos_list(request):
    """
    API endpoint para listar todos os blocos/locais disponíveis
    """
    blocos = [{'id': id, 'nome': nome} for id, nome in BLOCO_CHOICES]
    return Response(blocos)
