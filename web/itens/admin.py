"""
Configuração do painel administrativo para o sistema de Achados & Perdidos da UFT
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from itens.models import Item, Comentario

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Item
    """
    list_display = [
        'titulo', 'tipo_badge', 'categoria', 'bloco', 'status_badge', 
        'usuario', 'data_postagem', 'visualizacoes', 'prioridade_badge'
    ]
    list_filter = [
        'tipo', 'categoria', 'bloco', 'status', 'prioridade',
        'data_postagem', 'data_resolucao'
    ]
    search_fields = [
        'titulo', 'descricao', 'usuario__username', 
        'usuario__first_name', 'usuario__last_name'
    ]
    readonly_fields = [
        'data_postagem', 'data_atualizacao', 'visualizacoes'
    ]
    date_hierarchy = 'data_postagem'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'categoria', 'tipo', 'prioridade')
        }),
        ('Localização', {
            'fields': ('bloco', 'local_especifico')
        }),
        ('Datas', {
            'fields': ('data_ocorrencia', 'data_postagem', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
        ('Usuário e Status', {
            'fields': ('usuario', 'status', 'resolvido_por', 'data_resolucao')
        }),
        ('Contato', {
            'fields': ('telefone_contato', 'email_contato'),
            'classes': ('collapse',)
        }),
        ('Estatísticas', {
            'fields': ('visualizacoes',),
            'classes': ('collapse',)
        }),
    )
    
    actions = [
        'marcar_como_resolvido', 'marcar_como_spam', 'marcar_como_ativo',
        'marcar_como_prioritario', 'remover_prioridade'
    ]
    
    def tipo_badge(self, obj):
        """Exibe o tipo com badge colorido"""
        if obj.tipo == 'perdido':
            return format_html(
                '<span class="badge" style="background-color: #dc3545; color: white;">Perdido</span>'
            )
        else:
            return format_html(
                '<span class="badge" style="background-color: #28a745; color: white;">Encontrado</span>'
            )
    tipo_badge.short_description = 'Tipo'
    
    def status_badge(self, obj):
        """Exibe o status com badge colorido"""
        colors = {
            'ativo': '#007bff',
            'resolvido': '#28a745',
            'spam': '#dc3545',
            'expirado': '#6c757d'
        }
        return format_html(
            '<span class="badge" style="background-color: {}; color: white;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def prioridade_badge(self, obj):
        """Exibe indicador de prioridade"""
        if obj.prioridade:
            return format_html(
                '<span class="badge" style="background-color: #ff6b35; color: white;">PRIORITÁRIO</span>'
            )
        return '-'
    prioridade_badge.short_description = 'Prioridade'
    
    def marcar_como_resolvido(self, request, queryset):
        """Ação para marcar itens como resolvidos"""
        count = queryset.update(status='resolvido', data_resolucao=timezone.now())
        self.message_user(request, f'{count} itens marcados como resolvidos.')
    marcar_como_resolvido.short_description = "Marcar como resolvido"
    
    def marcar_como_spam(self, request, queryset):
        """Ação para marcar itens como spam"""
        count = queryset.update(status='spam')
        self.message_user(request, f'{count} itens marcados como spam.')
    marcar_como_spam.short_description = "Marcar como spam"
    
    def marcar_como_ativo(self, request, queryset):
        """Ação para marcar itens como ativos"""
        count = queryset.update(status='ativo')
        self.message_user(request, f'{count} itens marcados como ativos.')
    marcar_como_ativo.short_description = "Marcar como ativo"
    
    def marcar_como_prioritario(self, request, queryset):
        """Ação para marcar itens como prioritários"""
        count = queryset.update(prioridade=True)
        self.message_user(request, f'{count} itens marcados como prioritários.')
    marcar_como_prioritario.short_description = "Marcar como prioritário"
    
    def remover_prioridade(self, request, queryset):
        """Ação para remover prioridade dos itens"""
        count = queryset.update(prioridade=False)
        self.message_user(request, f'Prioridade removida de {count} itens.')
    remover_prioridade.short_description = "Remover prioridade"

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    """
    Configuração do admin para comentários
    """
    list_display = ['item_link', 'usuario', 'data_comentario', 'texto_resumido']
    list_filter = ['data_comentario']
    search_fields = ['texto', 'usuario__username', 'item__titulo']
    readonly_fields = ['data_comentario']
    date_hierarchy = 'data_comentario'
    
    def item_link(self, obj):
        """Link para o item comentado"""
        url = reverse('admin:itens_item_change', args=[obj.item.pk])
        return format_html('<a href="{}">{}</a>', url, obj.item.titulo)
    item_link.short_description = 'Item'
    
    def texto_resumido(self, obj):
        """Texto resumido do comentário"""
        return obj.texto[:50] + '...' if len(obj.texto) > 50 else obj.texto
    texto_resumido.short_description = 'Comentário'





# Admin para modelo de compatibilidade
# Fim das classes de administração

# Customizações gerais do admin
admin.site.site_header = "Sistema de Achados & Perdidos - UFT Palmas"
admin.site.site_title = "Achados & Perdidos UFT"
admin.site.index_title = "Painel de Administração"