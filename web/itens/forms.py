"""
Formulários do sistema de Achados & Perdidos da UFT Palmas
"""

from django import forms
from django.contrib.auth.models import User
from itens.models import (
    Item, Comentario, ReivindicacaoItem, PontoEncontro, Anuncio,
    TIPO_ITEM_CHOICES, CATEGORIA_CHOICES, BLOCO_CHOICES, STATUS_CHOICES
)

class FormularioItem(forms.ModelForm):
    """
    Formulário para cadastro e edição de itens perdidos/encontrados
    """
    
    class Meta:
        model = Item
        fields = [
            'titulo', 'descricao', 'categoria', 'tipo', 'bloco', 
            'local_especifico', 'data_ocorrencia', 
            'telefone_contato', 'email_contato', 'prioridade'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Ex: Celular Samsung Galaxy S21',
                'class': 'form-control'
            }),
            'descricao': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva o item com detalhes: cor, marca, características distintivas, etc.',
                'class': 'form-control'
            }),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'bloco': forms.Select(attrs={'class': 'form-control'}),
            'local_especifico': forms.TextInput(attrs={
                'placeholder': 'Ex: Sala 101, 2º andar, próximo ao bebedouro',
                'class': 'form-control'
            }),
            'data_ocorrencia': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'telefone_contato': forms.TextInput(attrs={
                'placeholder': '(63) 99999-9999',
                'class': 'form-control'
            }),
            'email_contato': forms.EmailInput(attrs={
                'placeholder': 'seu.email@uft.edu.br',
                'class': 'form-control'
            }),
            'prioridade': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'titulo': 'Título do Item',
            'descricao': 'Descrição Detalhada',
            'categoria': 'Categoria',
            'tipo': 'Tipo de Registro',
            'bloco': 'Local no Campus',
            'local_especifico': 'Detalhes do Local',
            'data_ocorrencia': 'Data/Hora da Ocorrência',
            'telefone_contato': 'Telefone (Opcional)',
            'email_contato': 'Email (Opcional)',
            'prioridade': 'Item Prioritário (documentos importantes, medicamentos, etc.)',
        }
        help_texts = {
            'titulo': 'Seja específico mas conciso',
            'descricao': 'Quanto mais detalhes, maior a chance de recuperação',
            'data_ocorrencia': 'Quando aproximadamente o item foi perdido/encontrado',
            'prioridade': 'Marque se for um item de extrema importância',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplicar classes CSS automaticamente
        for field_name, field in self.fields.items():
            if field_name != 'prioridade':  # Checkbox tem classe diferente
                field.widget.attrs.update({'class': 'form-control'})
    
    def clean_titulo(self):
        """Validação customizada para o título"""
        titulo = self.cleaned_data.get('titulo')
        if len(titulo) < 5:
            raise forms.ValidationError('O título deve ter pelo menos 5 caracteres.')
        return titulo.title()  # Capitaliza o título
    
    def clean_descricao(self):
        """Validação customizada para a descrição"""
        descricao = self.cleaned_data.get('descricao')
        if len(descricao) < 20:
            raise forms.ValidationError('A descrição deve ter pelo menos 20 caracteres para facilitar a identificação.')
        return descricao

class FormularioComentario(forms.ModelForm):
    """
    Formulário para adicionar comentários em itens
    """
    
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Compartilhe informações úteis sobre este item...',
                'class': 'form-control'
            })
        }
        labels = {
            'texto': 'Seu Comentário'
        }
    
    def clean_texto(self):
        """Validação para evitar comentários muito curtos"""
        texto = self.cleaned_data.get('texto')
        if len(texto.strip()) < 10:
            raise forms.ValidationError('O comentário deve ter pelo menos 10 caracteres.')
        return texto.strip()

class FormularioReivindicacao(forms.ModelForm):
    """
    Formulário para reivindicar um item encontrado
    """
    
    class Meta:
        model = ReivindicacaoItem
        fields = ['justificativa']
        widgets = {
            'justificativa': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva detalhes que comprovem que este item é seu: características específicas, onde perdeu, quando, etc.',
                'class': 'form-control'
            })
        }
        labels = {
            'justificativa': 'Por que este item é seu?'
        }
        help_texts = {
            'justificativa': 'Seja específico: mencione detalhes que só o dono saberia'
        }
    
    def clean_justificativa(self):
        """Validação para justificativa detalhada"""
        justificativa = self.cleaned_data.get('justificativa')
        if len(justificativa.strip()) < 30:
            raise forms.ValidationError('A justificativa deve ser mais detalhada (mínimo 30 caracteres).')
        return justificativa.strip()

class FormularioPontoEncontro(forms.ModelForm):
    """
    Formulário para agendar ponto de encontro
    """
    
    class Meta:
        model = PontoEncontro
        fields = ['local_encontro', 'data_encontro', 'observacoes']
        widgets = {
            'local_encontro': forms.Select(choices=[
                ('biblioteca', 'Biblioteca Central - Entrada Principal'),
                ('restaurante', 'Restaurante Universitário - Entrada'),
                ('bloco_1', 'Bloco 1 - Hall de Entrada'),
                ('bloco_2', 'Bloco 2 - Recepção'),
                ('bloco_3', 'Bloco 3 - Secretaria'),
                ('portaria', 'Portaria Principal'),
                ('area_convivencia', 'Área de Convivência'),
                ('outro', 'Outro Local (especificar nas observações)'),
            ], attrs={'class': 'form-control'}),
            'data_encontro': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Observações adicionais sobre o encontro (opcional)',
                'class': 'form-control'
            })
        }
        labels = {
            'local_encontro': 'Local do Encontro',
            'data_encontro': 'Data e Hora',
            'observacoes': 'Observações'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Definir data mínima como agora
        import datetime
        now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')
        self.fields['data_encontro'].widget.attrs['min'] = now

class FormularioFiltro(forms.Form):
    """
    Formulário para filtros de busca avançada
    """
    busca = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar por título, descrição ou local...',
            'class': 'form-control'
        }),
        label='Busca Geral'
    )
    
    tipo = forms.ChoiceField(
        choices=[('', 'Todos os Tipos')] + TIPO_ITEM_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo'
    )
    
    categoria = forms.ChoiceField(
        choices=[('', 'Todas as Categorias')] + CATEGORIA_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Categoria'
    )
    
    bloco = forms.ChoiceField(
        choices=[('', 'Todos os Locais')] + BLOCO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Local'
    )
    
    status = forms.ChoiceField(
        choices=[
            ('', 'Todos os Status'),
            ('ativo', 'Apenas Ativos'),
            ('resolvido', 'Apenas Resolvidos')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Status'
    )
    
    prioridade = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Apenas Prioritários'
    )
    
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Data Inicial'
    )
    
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label='Data Final'
    )

class FormularioRegistroUsuario(forms.ModelForm):
    """
    Formulário para registro de novos usuários
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Senha'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirmar Senha'
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome de usuário'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Primeiro nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sobrenome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seu.email@uft.edu.br'
            }),
        }
    
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('As senhas não coincidem.')
        
        return password_confirm
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está em uso.')
        return email

# Formulário de compatibilidade (será removido)
class FormularioAnuncio(forms.ModelForm):
    """
    Formulário para o modelo Anuncio (compatibilidade)
    DEPRECATED: Use FormularioItem
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = Anuncio
        exclude = ['usuario']