"""
Serializers para a API REST do Sistema de Achados & Perdidos
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from itens.models import Item, Comentario, ContatoItem


class TokenSerializer(serializers.Serializer):
    """Serializer para tokens JWT"""
    id = serializers.IntegerField(read_only=True)
    jti = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    expires_at = serializers.DateTimeField(read_only=True)
    blacklisted = serializers.BooleanField(read_only=True)


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer para criar novos usuários com tratamento adequado da senha
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
        read_only_fields = ['id']
        
    def validate(self, data):
        """
        Verifica se as senhas coincidem
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "As senhas não coincidem."})
        return data
    
    def create(self, validated_data):
        """
        Cria e retorna um novo usuário com senha criptografada
        """
        # Remove o campo password_confirm
        validated_data.pop('password_confirm')
        
        # Extrair os campos necessários
        username = validated_data['username']
        email = validated_data.get('email', '')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        
        # Usar create_user que já trata corretamente a senha
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Log de criação
        import logging
        logger = logging.getLogger('achados_perdidos_uft')
        logger.info(f'Novo usuário API criado: {username} ({email})')
        
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer para o modelo User do Django"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']
        

class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalhes do usuário"""
    
    itens_postados_count = serializers.SerializerMethodField()
    contatos_recebidos_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_joined', 'itens_postados_count', 'contatos_recebidos_count'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_itens_postados_count(self, obj):
        return obj.itens_postados.count()
    
    def get_contatos_recebidos_count(self, obj):
        return ContatoItem.objects.filter(item__usuario=obj).count()


class ComentarioSerializer(serializers.ModelSerializer):
    """Serializer para comentários em itens"""
    
    usuario_nome = serializers.SerializerMethodField()
    
    class Meta:
        model = Comentario
        fields = ['id', 'item', 'usuario', 'usuario_nome', 'texto', 'data_comentario']
        read_only_fields = ['id', 'usuario', 'data_comentario']
    
    def get_usuario_nome(self, obj):
        return f"{obj.usuario.first_name} {obj.usuario.last_name}".strip() or obj.usuario.username
        
    def create(self, validated_data):
        # Adiciona o usuário atual como autor do comentário
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)


class ContatoItemSerializer(serializers.ModelSerializer):
    """Serializer para contatos relacionados a itens"""
    
    usuario_interessado_nome = serializers.SerializerMethodField()
    
    class Meta:
        model = ContatoItem
        fields = ['id', 'item', 'usuario_interessado', 'usuario_interessado_nome', 
                 'mensagem', 'data_contato', 'visualizado']
        read_only_fields = ['id', 'usuario_interessado', 'data_contato']
    
    def get_usuario_interessado_nome(self, obj):
        return f"{obj.usuario_interessado.first_name} {obj.usuario_interessado.last_name}".strip() or obj.usuario_interessado.username
        
    def create(self, validated_data):
        # Adiciona o usuário atual como interessado
        validated_data['usuario_interessado'] = self.context['request'].user
        return super().create(validated_data)


class ItemSerializer(serializers.ModelSerializer):
    """Serializer básico para itens"""
    
    usuario_nome = serializers.SerializerMethodField()
    categoria_display = serializers.CharField(source='get_categoria_display', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    bloco_display = serializers.CharField(source='get_bloco_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    tempo_desde_postagem = serializers.CharField(read_only=True)
    
    class Meta:
        model = Item
        fields = [
            'id', 'titulo', 'descricao', 'categoria', 'categoria_display',
            'tipo', 'tipo_display', 'bloco', 'bloco_display',
            'local_especifico', 'foto', 'data_postagem', 'data_ocorrencia',
            'data_atualizacao', 'usuario', 'usuario_nome', 'status', 'status_display',
            'telefone_contato', 'email_contato', 'visualizacoes',
            'prioridade', 'tempo_desde_postagem'
        ]
        read_only_fields = ['id', 'data_postagem', 'data_atualizacao', 'usuario', 'visualizacoes']
    
    def get_usuario_nome(self, obj):
        return f"{obj.usuario.first_name} {obj.usuario.last_name}".strip() or obj.usuario.username
        
    def create(self, validated_data):
        # Adiciona o usuário atual como autor do item
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)


class ItemDetailSerializer(ItemSerializer):
    """Serializer detalhado para itens, incluindo comentários"""
    
    comentarios = ComentarioSerializer(many=True, read_only=True)
    contatos_count = serializers.SerializerMethodField()
    
    class Meta(ItemSerializer.Meta):
        fields = ItemSerializer.Meta.fields + ['comentarios', 'contatos_count']
    
    def get_contatos_count(self, obj):
        return obj.contatos.count()
