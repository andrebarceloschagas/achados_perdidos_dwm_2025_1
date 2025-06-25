"""
Configuração do app Itens para o Sistema de Achados & Perdidos
"""

from django.apps import AppConfig

class ItensConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'itens'
    verbose_name = 'Itens Perdidos e Encontrados'
    
    def ready(self):
        """
        Método executado quando o app está pronto
        Pode ser usado para registrar signals, etc.
        """
        pass
