"""
Modelos do sistema de Achados & Perdidos
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Choices para tipos de item
TIPO_ITEM_CHOICES = [
    ('perdido', 'Item Perdido'),
    ('encontrado', 'Item Encontrado'),
]

# Choices para status do item
STATUS_CHOICES = [
    ('ativo', 'Ativo'),
    ('resolvido', 'Resolvido'),
    ('spam', 'Spam'),
    ('expirado', 'Expirado'),
]

# Choices para blocos e locais da UFT Palmas
BLOCO_CHOICES = [
    ('bloco_1', 'Bloco 1'),
    ('bloco_2', 'Bloco 2'),
    ('bloco_3', 'Bloco 3'),
    ('bloco_a', 'Bloco A'),
    ('bloco_b', 'Bloco B'),
    ('bloco_c', 'Bloco C'),
    ('bloco_d', 'Bloco D'),
    ('bloco_e', 'Bloco E'),
    ('bloco_f', 'Bloco F'),
    ('bloco_g', 'Bloco G'),
    ('bloco_h', 'Bloco H'),
    ('bloco_i', 'Bloco I'),
    ('bloco_j', 'Bloco J'),
    ('calendoscopio', 'Calendoscópio/Jornalismo'),
    ('biblioteca', 'Biblioteca Central'),
    ('restaurante_ru', 'RU - Restaurante Universitário'),
    ('restaurante_fa', 'Restaurante Fazendinha'),
    ('secretaria', 'Secretaria Acadêmica'),
    ('coordenacao_ccomp', 'Coordenação de Curso Ciência da Computação'),
    ('ca_ccomp', 'CA - Centro Acadêmico de Ciência da Computação'),
    ('dojo', 'Dojô - Sala de Estudos'),
    ('diretoria', 'Diretoria do Campus de Palmas'),
    ('reitoria', 'Reitoria'),
    ('lanchonete', 'Lanchonete'),
    ('cuica', 'Cuica - CUICA'),
    ('labtec', 'LabTec'),
    ('prainha', 'Praianha'),
    ('pista_campo', 'Pista de Corrida/Campo de Futebol'),
    ('ponto_onibus', 'Ponto de Ônibus Principal'),
    ('ponto_onibus_reitoria', 'Ponto de Ônibus Reitoria'),
    ('ponto_onibus_j', 'Ponto de Ônibus Bloco J'),
    ('ponto_onibus_jornalismo', 'Ponto de Ônibus Jornalismo'),
    ('outro', 'Outro Local'),
]

# Choices para categorias de itens
CATEGORIA_CHOICES = [
    ('eletronicos', 'Eletrônicos'),
    ('documentos', 'Documentos'),
    ('roupas_acessorios', 'Roupas e Acessórios'),
    ('livros_material', 'Livros e Material Escolar'),
    ('chaves', 'Chaves'),
    ('carteira_bolsa', 'Carteira/Bolsa'),
    ('joias_bijuterias', 'Joias e Bijuterias'),
    ('oculos', 'Óculos'),
    ('equipamentos_esportivos', 'Equipamentos Esportivos'),
    ('instrumentos_musicais', 'Instrumentos Musicais'),
    ('medicamentos', 'Medicamentos'),
    ('outros', 'Outros'),
]

class ItemManager(models.Manager):
    """
    Manager customizado para o modelo Item
    """
    def ativos(self):
        """Retorna apenas itens ativos"""
        return self.filter(status='ativo')
    
    def perdidos(self):
        """Retorna apenas itens perdidos ativos"""
        return self.filter(tipo='perdido', status='ativo')
    
    def encontrados(self):
        """Retorna apenas itens encontrados ativos"""
        return self.filter(tipo='encontrado', status='ativo')
    
    def recentes(self, limite=10):
        """Retorna itens mais recentes"""
        return self.filter(status='ativo').order_by('-data_postagem')[:limite]

class Item(models.Model):
    """
    Modelo principal para itens perdidos e encontrados
    """
    # Informações básicas
    titulo = models.CharField(
        max_length=200, 
        help_text="Título descritivo do item (ex: 'Celular Samsung Galaxy')"
    )
    descricao = models.TextField(
        max_length=1000, 
        help_text="Descrição detalhada do item (cor, marca, características distintivas)"
    )
    categoria = models.CharField(
        max_length=30, 
        choices=CATEGORIA_CHOICES, 
        default='outros',
        help_text="Categoria do item para facilitar a busca"
    )
    tipo = models.CharField(
        max_length=10, 
        choices=TIPO_ITEM_CHOICES,
        help_text="Tipo do registro: item perdido ou encontrado"
    )
    
    # Localização no campus
    bloco = models.CharField(
        max_length=30, 
        choices=BLOCO_CHOICES,
        help_text="Local onde o item foi perdido ou encontrado"
    )
    local_especifico = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        help_text="Detalhes específicos do local (ex: 'Sala 101, 2º andar, próximo ao bebedouro')"
    )
    
    # Imagem do item
    foto = models.ImageField(
        upload_to='itens/fotos/', 
        blank=True, 
        null=True,
        help_text="Foto do item (opcional, mas recomendada)"
    )
    
    # Datas e timestamps
    data_postagem = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora em que o item foi cadastrado no sistema"
    )
    data_ocorrencia = models.DateTimeField(
        help_text="Data e hora aproximada em que o item foi perdido/encontrado"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        help_text="Última atualização do registro"
    )
    
    # Relacionamentos
    usuario = models.ForeignKey(
        User, 
        related_name='itens_postados', 
        on_delete=models.CASCADE,
        help_text="Usuário que cadastrou o item"
    )
    
    # Status e controle
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='ativo',
        help_text="Status atual do item"
    )
    resolvido_por = models.ForeignKey(
        User, 
        related_name='itens_resolvidos', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True,
        help_text="Usuário que ajudou a resolver o caso"
    )
    data_resolucao = models.DateTimeField(
        blank=True, 
        null=True,
        help_text="Data em que o item foi devolvido/recuperado"
    )
    
    # Informações de contato
    telefone_contato = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="Telefone para contato (opcional)"
    )
    email_contato = models.EmailField(
        blank=True, 
        null=True,
        help_text="Email para contato (opcional)"
    )
    
    # Campos adicionais para melhor controle
    visualizacoes = models.PositiveIntegerField(
        default=0,
        help_text="Número de visualizações do item"
    )
    prioridade = models.BooleanField(
        default=False,
        help_text="Marcar como prioritário (documentos importantes, medicamentos, etc.)"
    )
    
    # Manager customizado
    objects = ItemManager()
    
    class Meta:
        ordering = ['-data_postagem']
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'
        indexes = [
            models.Index(fields=['tipo', 'status']),
            models.Index(fields=['categoria']),
            models.Index(fields=['bloco']),
            models.Index(fields=['-data_postagem']),
        ]
    
    def __str__(self):
        return f'{self.get_tipo_display()}: {self.titulo} - {self.get_bloco_display()}'
    
    def get_absolute_url(self):
        """URL para visualizar o item"""
        return reverse('detalhe-item', kwargs={'pk': self.pk})
    
    def is_perdido(self):
        """Verifica se é um item perdido"""
        return self.tipo == 'perdido'
    
    def is_encontrado(self):
        """Verifica se é um item encontrado"""
        return self.tipo == 'encontrado'
    
    def is_resolvido(self):
        """Verifica se o item foi resolvido"""
        return self.status == 'resolvido'
    
    def is_prioritario(self):
        """Verifica se o item é prioritário"""
        return self.prioridade
    
    def marcar_como_resolvido(self, usuario=None):
        """Marca o item como resolvido"""
        self.status = 'resolvido'
        self.data_resolucao = timezone.now()
        if usuario:
            self.resolvido_por = usuario
        self.save()
    
    def incrementar_visualizacoes(self):
        """Incrementa o contador de visualizações"""
        self.visualizacoes += 1
        self.save(update_fields=['visualizacoes'])
    
    def dias_desde_postagem(self):
        """Retorna quantos dias se passaram desde a postagem"""
        return (timezone.now() - self.data_postagem).days
    
    def tempo_desde_postagem(self):
        """Retorna o tempo desde a postagem em formato legível"""
        delta = timezone.now() - self.data_postagem
        if delta.days > 0:
            return f"{delta.days} dia{'s' if delta.days != 1 else ''}"
        elif delta.seconds > 3600:
            horas = delta.seconds // 3600
            return f"{horas} hora{'s' if horas != 1 else ''}"
        else:
            minutos = delta.seconds // 60
            return f"{minutos} minuto{'s' if minutos != 1 else ''}"
    

    
    def pode_editar(self, usuario):
        """Verifica se o usuário pode editar este item"""
        return self.usuario == usuario or usuario.is_staff
    
    def contatos_nao_lidos(self):
        """Retorna o número de contatos não lidos para este item"""
        return self.contatos.filter(visualizado=False).count()


class Comentario(models.Model):
    """
    Modelo para comentários em itens
    """
    item = models.ForeignKey(
        Item, 
        related_name='comentarios', 
        on_delete=models.CASCADE
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(
        max_length=500,
        help_text="Comentário sobre o item (informações adicionais, dicas, etc.)"
    )
    data_comentario = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['data_comentario']
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
    
    def __str__(self):
        return f'Comentário de {self.usuario.username} em {self.item.titulo}'


class ContatoItem(models.Model):
    """
    Modelo para registrar contatos diretos entre usuários interessados e proprietários de itens
    """
    item = models.ForeignKey(
        Item,
        related_name='contatos',
        on_delete=models.CASCADE
    )
    usuario_interessado = models.ForeignKey(
        User,
        related_name='contatos_realizados',
        on_delete=models.CASCADE
    )
    mensagem = models.TextField(
        max_length=500,
        help_text="Mensagem para o proprietário do item"
    )
    data_contato = models.DateTimeField(auto_now_add=True)
    visualizado = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-data_contato']
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
        
    def __str__(self):
        return f'Contato de {self.usuario_interessado.username} sobre {self.item.titulo}'
