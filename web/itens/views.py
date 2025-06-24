"""
Views do sistema de Achados & Perdidos da UFT Palmas
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.conf import settings

from itens.models import Item, Comentario, Anuncio
from itens.forms import (
    FormularioItem, FormularioComentario, 
    FormularioFiltro, FormularioAnuncio
)
from achados_perdidos_uft.bibliotecas import LoginObrigatorio

class ListarItens(ListView):
    """
    View principal para listar itens perdidos/encontrados com filtros avançados
    """
    model = Item
    context_object_name = 'itens'
    template_name = 'itens/listar_itens.html'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Item.objects.filter(
            status__in=['ativo', 'resolvido']
        ).select_related('usuario').prefetch_related('comentarios')
        
        # Aplicar filtros de busca
        busca = self.request.GET.get('busca')
        if busca:
            queryset = queryset.filter(
                Q(titulo__icontains=busca) | 
                Q(descricao__icontains=busca) |
                Q(local_especifico__icontains=busca)
            )
        
        # Filtros específicos
        tipo = self.request.GET.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        
        categoria = self.request.GET.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        
        bloco = self.request.GET.get('bloco')
        if bloco:
            queryset = queryset.filter(bloco=bloco)
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        prioridade = self.request.GET.get('prioridade')
        if prioridade:
            queryset = queryset.filter(prioridade=True)
        
        # Filtros de data
        data_inicio = self.request.GET.get('data_inicio')
        if data_inicio:
            queryset = queryset.filter(data_postagem__date__gte=data_inicio)
        
        data_fim = self.request.GET.get('data_fim')
        if data_fim:
            queryset = queryset.filter(data_postagem__date__lte=data_fim)
        
        # Ordenação
        ordenacao = self.request.GET.get('ordenacao', '-data_postagem')
        if ordenacao in ['-data_postagem', 'data_postagem', 'titulo', '-visualizacoes']:
            queryset = queryset.order_by(ordenacao)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estatísticas para exibir no topo
        context['total_perdidos'] = Item.objects.filter(tipo='perdido', status='ativo').count()
        context['total_encontrados'] = Item.objects.filter(tipo='encontrado', status='ativo').count()
        context['total_resolvidos'] = Item.objects.filter(status='resolvido').count()
        
        # Formulário de filtros
        context['form_filtro'] = FormularioFiltro(self.request.GET)
        
        # Parâmetros de busca para manter nos links de paginação
        context['query_params'] = self.request.GET.urlencode()
        
        return context

class DetalheItem(DetailView):
    """
    View para exibir detalhes de um item específico
    """
    model = Item
    context_object_name = 'item'
    template_name = 'itens/detalhe_item.html'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Incrementar visualizações
        obj.incrementar_visualizacoes()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        
        # Formulários para interação
        context['form_comentario'] = FormularioComentario()
        
        # Comentários do item
        context['comentarios'] = item.comentarios.select_related('usuario').order_by('data_comentario')
        
        # Itens similares
        context['itens_similares'] = Item.objects.filter(
            categoria=item.categoria,
            status='ativo'
        ).exclude(pk=item.pk)[:4]
        
        return context

class CriarItem(LoginRequiredMixin, CreateView):
    """
    View para criar novo item perdido/encontrado
    """
    model = Item
    form_class = FormularioItem
    template_name = 'itens/novo_item.html'
    success_url = reverse_lazy('itens:listar-itens')
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(
            self.request, 
            f'Item "{form.instance.titulo}" cadastrado com sucesso!'
        )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Cadastrar Novo Item'
        return context

class EditarItem(LoginRequiredMixin, UpdateView):
    """
    View para editar item existente
    """
    model = Item
    form_class = FormularioItem
    template_name = 'itens/editar_item.html'
    
    def get_queryset(self):
        # Usuário só pode editar seus próprios itens (ou staff)
        if self.request.user.is_staff:
            return Item.objects.all()
        return Item.objects.filter(usuario=self.request.user)
    
    def form_valid(self, form):
        messages.success(
            self.request, 
            f'Item "{form.instance.titulo}" atualizado com sucesso!'
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('itens:detalhe-item', kwargs={'pk': self.object.pk})

class DeletarItem(LoginRequiredMixin, DeleteView):
    """
    View para deletar item
    """
    model = Item
    template_name = 'itens/deletar_item.html'
    success_url = reverse_lazy('itens:listar-itens')
    
    def get_queryset(self):
        # Usuário só pode deletar seus próprios itens (ou staff)
        if self.request.user.is_staff:
            return Item.objects.all()
        return Item.objects.filter(usuario=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        messages.success(request, f'Item "{item.titulo}" removido com sucesso!')
        return super().delete(request, *args, **kwargs)

@login_required
def adicionar_comentario(request, item_id):
    """
    View para adicionar comentário a um item
    """
    item = get_object_or_404(Item, pk=item_id)
    
    if request.method == 'POST':
        form = FormularioComentario(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.item = item
            comentario.usuario = request.user
            comentario.save()
            messages.success(request, 'Comentário adicionado com sucesso!')
        else:
            messages.error(request, 'Erro ao adicionar comentário. Verifique os dados.')
    
    return redirect('itens:detalhe-item', pk=item_id)





@login_required
def marcar_como_resolvido(request, item_id):
    """
    View para marcar item como resolvido
    """
    item = get_object_or_404(Item, pk=item_id)
    
    # Verificar permissão
    if item.usuario != request.user and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para esta ação.')
        return redirect('itens:detalhe-item', pk=item_id)
    
    item.marcar_como_resolvido(request.user)
    messages.success(request, f'Item "{item.titulo}" marcado como resolvido!')
    
    return redirect('itens:detalhe-item', pk=item_id)

@login_required
def meus_itens(request):
    """
    View para listar itens do usuário logado
    """
    itens = Item.objects.filter(usuario=request.user).order_by('-data_postagem')
    
    # Paginação
    paginator = Paginator(itens, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'itens': page_obj,
        'total_itens': itens.count(),
        'total_ativos': itens.filter(status='ativo').count(),
        'total_resolvidos': itens.filter(status='resolvido').count(),
    }
    
    return render(request, 'itens/meus_itens.html', context)









def itens_recentes_api(request):
    """
    API para retornar itens recentes (JSON)
    """
    itens = Item.objects.filter(status='ativo').order_by('-data_postagem')[:10]
    
    data = []
    for item in itens:
        data.append({
            'id': item.id,
            'titulo': item.titulo,
            'tipo': item.get_tipo_display(),
            'categoria': item.get_categoria_display(),
            'bloco': item.get_bloco_display(),
            'data_postagem': item.data_postagem.strftime('%d/%m/%Y %H:%M'),
            'url': reverse('itens:detalhe-item', kwargs={'pk': item.pk})
        })
    
    return JsonResponse({'itens': data})

# Views de compatibilidade (serão removidas)
class ListarAnuncios(ListView):
    """View de compatibilidade para anúncios antigos"""
    model = Anuncio
    context_object_name = 'anuncios'
    template_name = 'itens/listar.html'

class CriarAnuncios(LoginObrigatorio, CreateView):
    """View de compatibilidade para criar anúncios"""
    model = Anuncio
    form_class = FormularioAnuncio
    template_name = 'itens/novo.html'
    success_url = reverse_lazy('itens:listar-anuncios')
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class EditarAnuncios(LoginObrigatorio, UpdateView):
    """View de compatibilidade para editar anúncios"""
    model = Anuncio
    form_class = FormularioAnuncio
    template_name = 'itens/novo.html'
    success_url = reverse_lazy('itens:listar-anuncios')

class DeletarAnuncio(LoginObrigatorio, DeleteView):
    """View de compatibilidade para deletar anúncios"""
    model = Anuncio
    template_name = 'itens/deletar_item.html'
    success_url = reverse_lazy('itens:listar-anuncios')