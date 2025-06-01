"""
Configuração do painel administrativo para o sistema de Achados & Perdidos da UFT
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from itens.models import Item, Comentario, ReivindicacaoItem, PontoEncontro, Anuncio

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

@admin.register(ReivindicacaoItem)
class ReivindicacaoItemAdmin(admin.ModelAdmin):
    """
    Configuração do admin para reivindicações
    """
    list_display = [
        'item_link', 'usuario', 'data_reivindicacao', 
        'aprovada_badge', 'data_resposta'
    ]
    list_filter = ['aprovada', 'data_reivindicacao', 'data_resposta']
    search_fields = [
        'item__titulo', 'usuario__username', 'justificativa'
    ]
    readonly_fields = ['data_reivindicacao']
    date_hierarchy = 'data_reivindicacao'
    
    fieldsets = (
        ('Reivindicação', {
            'fields': ('item', 'usuario', 'justificativa', 'data_reivindicacao')
        }),
        ('Resposta da Administração', {
            'fields': ('aprovada', 'data_resposta', 'observacoes_admin')
        }),
    )
    
    actions = ['aprovar_reivindicacao', 'rejeitar_reivindicacao']
    
    def item_link(self, obj):
        """Link para o item reivindicado"""
        url = reverse('admin:itens_item_change', args=[obj.item.pk])
        return format_html('<a href="{}">{}</a>', url, obj.item.titulo)
    item_link.short_description = 'Item'
    
    def aprovada_badge(self, obj):
        """Badge para status da aprovação"""
        if obj.aprovada:
            return format_html(
                '<span class="badge" style="background-color: #28a745; color: white;">Aprovada</span>'
            )
        elif obj.data_resposta:
            return format_html(
                '<span class="badge" style="background-color: #dc3545; color: white;">Rejeitada</span>'
            )
        else:
            return format_html(
                '<span class="badge" style="background-color: #ffc107; color: black;">Pendente</span>'
            )
    aprovada_badge.short_description = 'Status'
    
    def aprovar_reivindicacao(self, request, queryset):
        """Ação para aprovar reivindicações"""
        count = queryset.update(aprovada=True, data_resposta=timezone.now())
        self.message_user(request, f'{count} reivindicações aprovadas.')
    aprovar_reivindicacao.short_description = "Aprovar reivindicação"
    
    def rejeitar_reivindicacao(self, request, queryset):
        """Ação para rejeitar reivindicações"""
        count = queryset.update(aprovada=False, data_resposta=timezone.now())
        self.message_user(request, f'{count} reivindicações rejeitadas.')
    rejeitar_reivindicacao.short_description = "Rejeitar reivindicação"

@admin.register(PontoEncontro)
class PontoEncontroAdmin(admin.ModelAdmin):
    """
    Configuração do admin para pontos de encontro
    """
    list_display = [
        'item_link', 'usuario_solicitante', 'usuario_postador', 
        'data_encontro', 'status_encontro', 'realizado'
    ]
    list_filter = [
        'realizado', 'confirmado_solicitante', 'confirmado_postador', 
        'data_encontro', 'data_criacao'
    ]
    search_fields = [
        'item__titulo', 'usuario_solicitante__username', 
        'usuario_postador__username', 'local_encontro'
    ]
    readonly_fields = ['data_criacao']
    date_hierarchy = 'data_encontro'
    
    def item_link(self, obj):
        """Link para o item do encontro"""
        url = reverse('admin:itens_item_change', args=[obj.item.pk])
        return format_html('<a href="{}">{}</a>', url, obj.item.titulo)
    item_link.short_description = 'Item'
    
    def status_encontro(self, obj):
        """Status do encontro"""
        if obj.realizado:
            return format_html(
                '<span class="badge" style="background-color: #28a745; color: white;">Realizado</span>'
            )
        elif obj.is_confirmado():
            return format_html(
                '<span class="badge" style="background-color: #007bff; color: white;">Confirmado</span>'
            )
        else:
            return format_html(
                '<span class="badge" style="background-color: #ffc107; color: black;">Pendente</span>'
            )
    status_encontro.short_description = 'Status'

# Admin para modelo de compatibilidade
@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    """
    Admin para modelo legado (compatibilidade)
    """
    list_display = ['data', 'descricao', 'preco', 'usuario']
    search_fields = ['descricao', 'usuario__username']
    list_filter = ['data']
    readonly_fields = ['data']
    
    def get_model_perms(self, request):
        """Oculta o modelo do menu principal (deprecated)"""
        return {}

# Customizações gerais do admin
admin.site.site_header = "Sistema de Achados & Perdidos - UFT Palmas"
admin.site.site_title = "Achados & Perdidos UFT"
admin.site.index_title = "Painel de Administração"