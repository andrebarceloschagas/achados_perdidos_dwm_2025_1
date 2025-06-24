"""
Context Processors para o sistema de Achados & Perdidos da UFT Palmas
"""

from django.db.models import Count, Q
from itens.models import ContatoItem

def notificacoes_usuario(request):
    """
    Adiciona contagem de notificações ao contexto global dos templates
    """
    context = {
        'total_contatos_nao_lidos': 0
    }
    
    if request.user.is_authenticated:
        # Contagem de contatos não lidos para itens do usuário
        contatos_nao_lidos = ContatoItem.objects.filter(
            item__usuario=request.user,
            visualizado=False
        ).count()
        
        context['total_contatos_nao_lidos'] = contatos_nao_lidos
    
    return context
