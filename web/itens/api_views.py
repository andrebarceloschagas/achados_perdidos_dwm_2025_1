"""
API Views para o sistema de Achados & Perdidos

Este módulo contém as views baseadas em classes da API REST
para interagir com os modelos do sistema.
"""

from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from itens.models import Item, Comentario, ContatoItem
from itens.serializers import (
    UserSerializer, UserDetailSerializer, CreateUserSerializer, ItemSerializer, 
    ItemDetailSerializer, ComentarioSerializer, ContatoItemSerializer,
    TokenSerializer
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada para permitir apenas proprietários de objetos
    para editá-los ou excluí-los.
    """
    
    def has_object_permission(self, request, view, obj):
        # Permite métodos seguros (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Verifica se o objeto tem um atributo 'usuario'
        if hasattr(obj, 'usuario'):
            return obj.usuario == request.user
        
        # Verifica se o objeto tem um atributo 'usuario_interessado'
        if hasattr(obj, 'usuario_interessado'):
            return obj.usuario_interessado == request.user
            
        # Para o modelo User
        return obj == request.user


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint para usuários:
    - Criação de conta (sem autenticação)
    - Listar/visualizar (com autenticação)
    """
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        """
        - Para criação de usuário: CreateUserSerializer
        - Para visualização detalhada: UserDetailSerializer
        - Para outros casos: UserSerializer
        """
        if self.action == 'create':
            return CreateUserSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer
    
    def get_permissions(self):
        """
        - Para criar usuário (POST): AllowAny
        - Para outras operações: IsAuthenticated
        """
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Endpoint para obter informações do usuário logado"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Endpoint para atualizar o perfil do usuário logado"""
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def tokens(self, request):
        """Endpoint para obter tokens ativos do usuário logado"""
        from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
        
        user_tokens = OutstandingToken.objects.filter(
            user=request.user,
        ).order_by('-created_at')
        
        # Formatar os tokens para retorno
        tokens_data = []
        for token in user_tokens:
            tokens_data.append({
                'id': token.id,
                'jti': token.jti, 
                'token': str(token.token)[:20] + '...',  # Truncado por segurança
                'created_at': token.created_at,
                'expires_at': token.expires_at,
                'blacklisted': hasattr(token, 'blacklistedtoken')
            })
        
        serializer = TokenSerializer(tokens_data, many=True)
        return Response({
            'count': len(tokens_data),
            'tokens': serializer.data
        })


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint para operações CRUD em itens
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'categoria', 'bloco', 'status', 'prioridade']
    search_fields = ['titulo', 'descricao', 'local_especifico']
    ordering_fields = ['data_postagem', 'data_ocorrencia', 'visualizacoes']
    ordering = ['-data_postagem']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ItemDetailSerializer
        return ItemSerializer
    
    def get_queryset(self):
        """Personaliza a queryset com filtros adicionais"""
        queryset = Item.objects.all()
        
        # Filtro por tipo (perdido/encontrado)
        tipo = self.request.query_params.get('tipo', None)
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        
        # Filtro por status (padrão: ativos)
        status_filter = self.request.query_params.get('status', 'ativo')
        if status_filter != 'todos':
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def perform_create(self, serializer):
        """Adiciona o usuário atual ao criar um item"""
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def meus_itens(self, request):
        """Endpoint para listar os itens do usuário logado"""
        itens = Item.objects.filter(usuario=request.user)
        page = self.paginate_queryset(itens)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(itens, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def marcar_resolvido(self, request, pk=None):
        """Endpoint para marcar um item como resolvido"""
        item = self.get_object()
        
        if item.usuario != request.user:
            return Response(
                {"detail": "Apenas o proprietário pode marcar como resolvido."}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        item.marcar_como_resolvido(request.user)
        serializer = self.get_serializer(item)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def incrementar_visualizacoes(self, request, pk=None):
        """Endpoint para incrementar visualizações de um item"""
        item = self.get_object()
        item.incrementar_visualizacoes()
        return Response({"visualizacoes": item.visualizacoes})
    
    @action(detail=False, methods=['get'])
    def itens_recentes(self, request):
        """Endpoint para obter itens recentes"""
        limite = int(request.query_params.get('limite', 10))
        itens = Item.objects.filter(status='ativo').order_by('-data_postagem')[:limite]
        serializer = ItemSerializer(itens, many=True)
        return Response(serializer.data)


class ComentarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para operações CRUD em comentários
    """
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """Filtra comentários por item_id se fornecido"""
        queryset = Comentario.objects.all()
        item_id = self.request.query_params.get('item_id', None)
        
        if item_id:
            queryset = queryset.filter(item_id=item_id)
            
        return queryset
    
    def perform_create(self, serializer):
        """Adiciona o usuário atual ao criar um comentário"""
        serializer.save(usuario=self.request.user)


class ContatoItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint para operações CRUD em contatos de itens
    """
    queryset = ContatoItem.objects.all()
    serializer_class = ContatoItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Limita os contatos que um usuário pode ver"""
        user = self.request.user
        
        # Se for um item do usuário, vê todos os contatos recebidos
        # Se for um contato feito pelo usuário, vê apenas os seus
        return ContatoItem.objects.filter(
            Q(item__usuario=user) | Q(usuario_interessado=user)
        )
    
    def perform_create(self, serializer):
        """Adiciona o usuário atual ao criar um contato"""
        serializer.save(usuario_interessado=self.request.user)
    
    @action(detail=False, methods=['get'])
    def contatos_recebidos(self, request):
        """Endpoint para listar os contatos recebidos nos itens do usuário"""
        contatos = ContatoItem.objects.filter(item__usuario=request.user).order_by('-data_contato')
        page = self.paginate_queryset(contatos)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(contatos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def contatos_enviados(self, request):
        """Endpoint para listar os contatos enviados pelo usuário"""
        contatos = ContatoItem.objects.filter(usuario_interessado=request.user).order_by('-data_contato')
        page = self.paginate_queryset(contatos)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(contatos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def marcar_visualizado(self, request, pk=None):
        """Endpoint para marcar um contato como visualizado"""
        contato = self.get_object()
        
        # Apenas o dono do item pode marcar como visualizado
        if contato.item.usuario != request.user:
            return Response(
                {"detail": "Apenas o proprietário do item pode marcar contatos como visualizados."}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        contato.visualizado = True
        contato.save()
        return Response({"status": "visualizado"})
    
    @action(detail=False, methods=['get'])
    def nao_lidos_count(self, request):
        """Endpoint para contar contatos não lidos"""
        count = ContatoItem.objects.filter(item__usuario=request.user, visualizado=False).count()
        return Response({"count": count})
