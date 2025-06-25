"""
Views principais do Sistema de Achados & Perdidos
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import View
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger('achados_perdidos_uft')

class PaginaInicial(View):
    """
    Página inicial do sistema com estatísticas e itens recentes
    """
    def get(self, request):
        # Importar aqui para evitar circular import
        from itens.models import Item
        
        # Calcular estatísticas do sistema
        total_perdidos = Item.objects.filter(tipo='perdido', status='ativo').count()
        total_encontrados = Item.objects.filter(tipo='encontrado', status='ativo').count()
        total_resolvidos = Item.objects.filter(status='resolvido').count()
        total_usuarios = User.objects.filter(is_active=True).count()
        
        # Itens recentes para exibir na página inicial
        itens_recentes = Item.objects.filter(status='ativo').order_by('-data_postagem')[:6]
        
        # Estatísticas por categoria
        categorias_populares = Item.objects.filter(status='ativo').values('categoria').distinct()[:5]
        
        contexto = {
            'total_perdidos': total_perdidos,
            'total_encontrados': total_encontrados,
            'total_resolvidos': total_resolvidos,
            'total_usuarios': total_usuarios,
            'itens_recentes': itens_recentes,
            'categorias_populares': categorias_populares,
            'campus': 'Campus Palmas',
            'universidade': 'Universidade Federal do Tocantins',
        }
        
        return render(request, 'index.html', contexto)

class LoginView(View):
    """
    View para autenticação de usuários da UFT
    """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        
        contexto = {
            'mensagem': '',
            'campus': 'Campus Palmas',
            'universidade': 'UFT',
        }
        return render(request, 'autenticacao.html', contexto)
    
    def post(self, request):
        # Obtém as credenciais de autenticação do formulário
        usuario = request.POST.get('usuario', '').strip()
        senha = request.POST.get('senha', '')

        if not usuario or not senha:
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'autenticacao.html', {'mensagem': 'Campos obrigatórios não preenchidos!'})

        logger.info(f'Tentativa de login para usuário: {usuario}')

        # Verifica se as credenciais são válidas
        user = authenticate(request, username=usuario, password=senha)
        
        if user is not None:
            # Verifica se o usuário está ativo
            if user.is_active:
                login(request, user)
                messages.success(request, f'Bem-vindo(a), {user.first_name or user.username}!')
                
                # Redireciona para a página solicitada ou página inicial
                next_page = request.GET.get('next', '/')
                return redirect(next_page)
            else:
                logger.warning(f'Tentativa de login com usuário inativo: {usuario}')
                return render(request, 'autenticacao.html', {
                    'mensagem': 'Sua conta está inativa. Entre em contato com a administração.'
                })
        else:
            logger.warning(f'Tentativa de login com credenciais inválidas: {usuario}')
            return render(request, 'autenticacao.html', {
                'mensagem': 'Usuário ou senha incorretos. Verifique suas credenciais.'
            })

class LogoutView(View):
    """
    View para logout de usuários
    """
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            logout(request)
            messages.info(request, f'Logout realizado com sucesso. Até logo, {username}!')
            logger.info(f'Logout realizado para usuário: {username}')
        
        # Redireciona para a página inicial
        return redirect('pagina-inicial')

class SobreView(View):
    """
    Página com informações sobre o sistema e a UFT
    """
    def get(self, request):
        contexto = {
            'campus': 'Campus Palmas',
            'universidade': 'Universidade Federal do Tocantins',
            'sigla': 'UFT',
        }
        return render(request, 'sobre.html', contexto)

class RegistroView(View):
    """
    View para registro de novos usuários da UFT
    """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        
        contexto = {
            'campus': 'Campus Palmas',
            'universidade': 'UFT',
        }
        return render(request, 'registro.html', contexto)
    
    def post(self, request):
        # Obtém os dados do formulário
        nome_completo = request.POST.get('nome_completo', '').strip()
        email = request.POST.get('email', '').strip()
        usuario = request.POST.get('usuario', '').strip()
        senha = request.POST.get('senha', '')
        confirmar_senha = request.POST.get('confirmar_senha', '')

        # Validações básicas
        if not all([nome_completo, email, usuario, senha, confirmar_senha]):
            messages.error(request, 'Por favor, preencha todos os campos.')
            return render(request, 'registro.html', {
                'mensagem': 'Todos os campos são obrigatórios!',
                'nome_completo': nome_completo,
                'email': email,
                'usuario': usuario
            })

        # Validar email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Por favor, insira um email válido.')
            return render(request, 'registro.html', {
                'mensagem': 'Email inválido!',
                'nome_completo': nome_completo,
                'email': email,
                'usuario': usuario
            })

        # Verificar se as senhas coincidem
        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'registro.html', {
                'mensagem': 'As senhas não coincidem!',
                'nome_completo': nome_completo,
                'email': email,
                'usuario': usuario
            })

        # Verificar se a senha tem pelo menos 6 caracteres
        if len(senha) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
            return render(request, 'registro.html', {
                'mensagem': 'A senha deve ter pelo menos 6 caracteres!',
                'nome_completo': nome_completo,
                'email': email,
                'usuario': usuario
            })

        # Verificar se o usuário já existe
        if User.objects.filter(username=usuario).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
            return render(request, 'registro.html', {
                'mensagem': 'Nome de usuário já existe!',
                'nome_completo': nome_completo,
                'email': email,
                'usuario': usuario
            })

        # Verificar se o email já está em uso
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está cadastrado.')
            return render(request, 'registro.html', {
                'mensagem': 'Email já cadastrado!',
                'nome_completo': nome_completo,
                'email': email,
                'usuario': usuario
            })

        try:
            # Criar o usuário
            user = User.objects.create_user(
                username=usuario,
                email=email,
                password=senha,
                first_name=nome_completo.split()[0] if nome_completo else '',
                last_name=' '.join(nome_completo.split()[1:]) if len(nome_completo.split()) > 1 else ''
            )
            
            logger.info(f'Novo usuário registrado: {usuario} ({email})')
            
            # Fazer login automático após o registro
            login(request, user)
            messages.success(request, f'Conta criada com sucesso! Bem-vindo(a), {user.first_name}!')
            
            return redirect('/')
            
        except Exception as e:
            logger.error(f'Erro ao criar usuário {usuario}: {str(e)}')
            messages.error(request, 'Erro interno. Tente novamente mais tarde.')
            return render(request, 'registro.html', {
                'mensagem': 'Erro ao criar conta. Tente novamente.',
                'nome_completo': nome_completo,
                'email': email,
                'usuario': usuario
            })
