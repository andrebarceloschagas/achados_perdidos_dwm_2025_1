"""
Configuração de aplicação para o projeto achados_perdidos_uft
"""

from django.apps import AppConfig


class AchadosPerdidosConfig(AppConfig):
    """
    Configuração da aplicação principal
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'achados_perdidos_uft'
    verbose_name = "Sistema de Achados & Perdidos UFT Palmas"

    def ready(self):
        """
        Método executado quando a aplicação é inicializada
        """
        # Importa as configurações de admin para JWT
        try:
            import achados_perdidos_uft.jwt_admin
        except ImportError:
            pass
