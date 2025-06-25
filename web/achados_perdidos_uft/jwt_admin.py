"""
Configuração do painel administrativo para os modelos de token JWT do Sistema de Achados & Perdidos
"""

from django.contrib import admin
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

class CustomOutstandingTokenAdmin(OutstandingTokenAdmin):
    """
    Configuração personalizada para o admin de OutstandingToken
    
    Remove a restrição de apenas leitura para permitir a exclusão de tokens
    """
    readonly_fields = ()  # Remove o comportamento padrão que impede a exclusão
    
    def has_delete_permission(self, *args, **kwargs):
        """Permite a exclusão de tokens no painel administrativo"""
        return True

# Desregistra o admin padrão e registra o personalizado
admin.site.unregister(OutstandingToken)
admin.site.register(OutstandingToken, CustomOutstandingTokenAdmin)

@admin.register(BlacklistedToken)
class BlacklistedTokenAdmin(admin.ModelAdmin):
    """
    Configuração do admin para tokens na blacklist
    """
    list_display = ['token', 'blacklisted_at', 'expires_at']
    list_filter = ['blacklisted_at']
    search_fields = ['token__jti', 'token__user__username']
    
    def expires_at(self, obj):
        """Mostra quando o token expira"""
        return obj.token.expires_at
    expires_at.short_description = "Expira em"
