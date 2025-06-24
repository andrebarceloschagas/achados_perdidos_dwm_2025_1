"""
Testes unitários para o sistema de Achados & Perdidos da UFT Palmas
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from itens.models import Item, Comentario
from itens.forms import FormularioItem, FormularioComentario



class ItemModelTest(TestCase):
    """Testes unitários para o modelo Item"""
    
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='testuser',
            email='test@uft.edu.br',
            password='testpass123'
        )
        
        self.item = Item.objects.create(
            titulo='Celular Samsung',
            descricao='Celular Samsung Galaxy S21 preto perdido na biblioteca',
            categoria='eletronicos',
            tipo='perdido',
            bloco='biblioteca',
            data_ocorrencia=timezone.now() - timedelta(hours=2),
            usuario=self.usuario,
            telefone_contato='(63) 99999-9999',
            email_contato='test@uft.edu.br'
        )
    
    def test_criacao_item(self):
        """Testa criação de item"""
        self.assertEqual(self.item.titulo, 'Celular Samsung')
        self.assertEqual(self.item.tipo, 'perdido')
        self.assertEqual(self.item.status, 'ativo')
        self.assertFalse(self.item.prioridade)
    
    def test_str_representation(self):
        """Testa representação string do item"""
        expected = "Item Perdido: Celular Samsung - Biblioteca Central"
        self.assertEqual(str(self.item), expected)
    
    def test_incrementar_visualizacoes(self):
        """Testa incremento de visualizações"""
        inicial = self.item.visualizacoes
        self.item.incrementar_visualizacoes()
        self.assertEqual(self.item.visualizacoes, inicial + 1)
    
    def test_marcar_como_resolvido(self):
        """Testa marcar item como resolvido"""
        outro_usuario = User.objects.create_user(username='outro', password='pass123')
        self.item.marcar_como_resolvido(outro_usuario)
        
        self.assertEqual(self.item.status, 'resolvido')
        self.assertEqual(self.item.resolvido_por, outro_usuario)
        self.assertIsNotNone(self.item.data_resolucao)
    
    def test_tempo_desde_postagem(self):
        """Testa cálculo de tempo desde postagem"""
        tempo = self.item.tempo_desde_postagem()
        self.assertIsInstance(tempo, str)
        self.assertTrue(len(tempo) > 0)
    



class ComentarioModelTest(TestCase):
    """Testes unitários para o modelo Comentario"""
    
    def setUp(self):
        self.usuario = User.objects.create_user(username='user', password='pass')
        self.item = Item.objects.create(
            titulo='Item Teste',
            descricao='Descrição teste',
            categoria='outros',
            tipo='perdido',
            bloco='bloco_1',
            data_ocorrencia=timezone.now(),
            usuario=self.usuario
        )
        self.comentario = Comentario.objects.create(
            item=self.item,
            usuario=self.usuario,
            texto='Comentário de teste'
        )
    
    def test_criacao_comentario(self):
        """Testa criação de comentário"""
        self.assertEqual(self.comentario.texto, 'Comentário de teste')
        self.assertEqual(self.comentario.item, self.item)
        self.assertEqual(self.comentario.usuario, self.usuario)
    
    def test_str_representation(self):
        """Testa representação string do comentário"""
        expected = f"Comentário de {self.usuario.username} em {self.item.titulo}"
        self.assertEqual(str(self.comentario), expected)





class FormularioItemTest(TestCase):
    """Testes unitários para FormularioItem"""
    
    def test_formulario_valido(self):
        """Testa formulário com dados válidos"""
        form_data = {
            'titulo': 'Carteira Perdida',
            'descricao': 'Carteira de couro marrom perdida na cantina',
            'categoria': 'documentos',
            'tipo': 'perdido',
            'bloco': 'restaurante_ru',
            'data_ocorrencia': timezone.now(),
            'telefone_contato': '(63) 99999-9999',
            'email_contato': 'test@uft.edu.br'
        }
        
        form = FormularioItem(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_formulario_titulo_obrigatorio(self):
        """Testa que título é obrigatório"""
        form_data = {
            'descricao': 'Descrição válida',
            'categoria': 'outros',
            'tipo': 'perdido',
            'bloco': 'bloco_1',
            'data_ocorrencia': timezone.now()
        }
        
        form = FormularioItem(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors)
    
    def test_formulario_descricao_obrigatoria(self):
        """Testa que descrição é obrigatória"""
        form_data = {
            'titulo': 'Título Válido',
            'categoria': 'outros',
            'tipo': 'perdido',
            'bloco': 'bloco_1',
            'data_ocorrencia': timezone.now()
        }
        
        form = FormularioItem(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('descricao', form.errors)
    
    def test_formulario_categoria_obrigatoria(self):
        """Testa que categoria é obrigatória"""
        form_data = {
            'titulo': 'Título Válido',
            'descricao': 'Descrição válida',
            'tipo': 'perdido',
            'bloco': 'bloco_1',
            'data_ocorrencia': timezone.now()
        }
        
        form = FormularioItem(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('categoria', form.errors)


class FormularioComentarioTest(TestCase):
    """Testes unitários para FormularioComentario"""
    
    def test_formulario_comentario_valido(self):
        """Testa formulário de comentário válido"""
        form_data = {
            'texto': 'Este é um comentário válido com texto suficiente'
        }
        
        form = FormularioComentario(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_formulario_comentario_texto_obrigatorio(self):
        """Testa que texto do comentário é obrigatório"""
        form_data = {}
        
        form = FormularioComentario(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('texto', form.errors)


class ItemManagerTest(TestCase):
    """Testes unitários para o manager do modelo Item"""
    
    def setUp(self):
        self.usuario = User.objects.create_user(username='user', password='pass')
        
        # Criar itens de teste
        Item.objects.create(
            titulo='Item Perdido',
            descricao='Descrição',
            categoria='outros',
            tipo='perdido',
            bloco='bloco_1',
            data_ocorrencia=timezone.now(),
            usuario=self.usuario
        )
        
        Item.objects.create(
            titulo='Item Encontrado',
            descricao='Descrição',
            categoria='outros',
            tipo='encontrado',
            bloco='bloco_1',
            data_ocorrencia=timezone.now(),
            usuario=self.usuario
        )
    
    def test_manager_todos_itens(self):
        """Testa que manager retorna todos os itens"""
        self.assertEqual(Item.objects.count(), 2)
    
    def test_filtro_por_tipo(self):
        """Testa filtro por tipo de item"""
        perdidos = Item.objects.filter(tipo='perdido')
        encontrados = Item.objects.filter(tipo='encontrado')
        
        self.assertEqual(perdidos.count(), 1)
        self.assertEqual(encontrados.count(), 1)
    
    def test_filtro_por_status(self):
        """Testa filtro por status de item"""
        ativos = Item.objects.filter(status='ativo')
        self.assertEqual(ativos.count(), 2)
