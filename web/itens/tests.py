"""
Testes para o sistema de Achados & Perdidos da UFT Palmas
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from itens.models import Item, Comentario, ReivindicacaoItem, PontoEncontro
from itens.forms import FormularioItem, FormularioComentario, FormularioReivindicacao

class ItemModelTest(TestCase):
    """
    Testes para o modelo Item
    """
    
    def setUp(self):
        """Configuração inicial para os testes"""
        self.usuario = User.objects.create_user(
            username='testuser',
            email='test@uft.edu.br',
            password='testpass123'
        )
        
        self.item_perdido = Item.objects.create(
            titulo='Celular Samsung',
            descricao='Celular Samsung Galaxy S21 preto perdido na biblioteca',
            categoria='eletronicos',
            tipo='perdido',
            bloco='biblioteca',
            local_especifico='2º andar, próximo aos computadores',
            data_ocorrencia=timezone.now() - timedelta(hours=2),
            usuario=self.usuario,
            telefone_contato='(63) 99999-9999',
            email_contato='test@uft.edu.br'
        )
        
        self.item_encontrado = Item.objects.create(
            titulo='Chaves UFT',
            descricao='Chaveiro com chaves da UFT encontrado no estacionamento',
            categoria='chaves',
            tipo='encontrado',
            bloco='estacionamento',
            local_especifico='Próximo ao portão principal',
            data_ocorrencia=timezone.now() - timedelta(hours=1),
            usuario=self.usuario
        )
    
    def test_criacao_item(self):
        """Testa a criação de um item"""
        self.assertEqual(self.item_perdido.titulo, 'Celular Samsung')
        self.assertEqual(self.item_perdido.tipo, 'perdido')
        self.assertEqual(self.item_perdido.status, 'ativo')
        self.assertFalse(self.item_perdido.prioridade)
    
    def test_str_representation(self):
        """Testa a representação string do item"""
        expected = f"[PERDIDO] Celular Samsung - {self.usuario.username}"
        self.assertEqual(str(self.item_perdido), expected)
    
    def test_incrementar_visualizacoes(self):
        """Testa o incremento de visualizações"""
        visualizacoes_inicial = self.item_perdido.visualizacoes
        self.item_perdido.incrementar_visualizacoes()
        self.assertEqual(self.item_perdido.visualizacoes, visualizacoes_inicial + 1)
    
    def test_marcar_como_resolvido(self):
        """Testa marcar item como resolvido"""
        outro_usuario = User.objects.create_user(
            username='outro_user',
            password='pass123'
        )
        
        self.item_perdido.marcar_como_resolvido(outro_usuario)
        self.assertEqual(self.item_perdido.status, 'resolvido')
        self.assertEqual(self.item_perdido.resolvido_por, outro_usuario)
        self.assertIsNotNone(self.item_perdido.data_resolucao)
    
    def test_tempo_desde_postagem(self):
        """Testa o cálculo do tempo desde a postagem"""
        tempo = self.item_perdido.tempo_desde_postagem()
        self.assertIn('minuto', tempo.lower())
    
    def test_pode_ser_reivindicado(self):
        """Testa se item pode ser reivindicado"""
        self.assertFalse(self.item_perdido.pode_ser_reivindicado())  # Item perdido
        self.assertTrue(self.item_encontrado.pode_ser_reivindicado())  # Item encontrado
        
        # Marcar como resolvido
        self.item_encontrado.marcar_como_resolvido(self.usuario)
        self.assertFalse(self.item_encontrado.pode_ser_reivindicado())  # Resolvido

class ComentarioModelTest(TestCase):
    """
    Testes para o modelo Comentario
    """
    
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.item = Item.objects.create(
            titulo='Item Teste',
            descricao='Descrição do item teste',
            categoria='outros',
            tipo='perdido',
            bloco='bloco_1',
            usuario=self.usuario
        )
        
        self.comentario = Comentario.objects.create(
            item=self.item,
            usuario=self.usuario,
            texto='Este é um comentário de teste'
        )
    
    def test_criacao_comentario(self):
        """Testa a criação de um comentário"""
        self.assertEqual(self.comentario.texto, 'Este é um comentário de teste')
        self.assertEqual(self.comentario.item, self.item)
        self.assertEqual(self.comentario.usuario, self.usuario)
    
    def test_str_representation(self):
        """Testa a representação string do comentário"""
        expected = f"Comentário de {self.usuario.username} em {self.item.titulo}"
        self.assertEqual(str(self.comentario), expected)

class ReivindicacaoItemModelTest(TestCase):
    """
    Testes para o modelo ReivindicacaoItem
    """
    
    def setUp(self):
        self.usuario_postador = User.objects.create_user(
            username='postador',
            password='pass123'
        )
        
        self.usuario_reivindicador = User.objects.create_user(
            username='reivindicador',
            password='pass123'
        )
        
        self.item = Item.objects.create(
            titulo='Item Encontrado',
            descricao='Item encontrado para teste',
            categoria='outros',
            tipo='encontrado',
            bloco='bloco_1',
            usuario=self.usuario_postador
        )
        
        self.reivindicacao = ReivindicacaoItem.objects.create(
            item=self.item,
            usuario=self.usuario_reivindicador,
            justificativa='Este item é meu porque tem minhas iniciais gravadas'
        )
    
    def test_criacao_reivindicacao(self):
        """Testa a criação de uma reivindicação"""
        self.assertEqual(self.reivindicacao.item, self.item)
        self.assertEqual(self.reivindicacao.usuario, self.usuario_reivindicador)
        self.assertIsNone(self.reivindicacao.aprovada)
        self.assertIsNone(self.reivindicacao.data_resposta)
    
    def test_str_representation(self):
        """Testa a representação string da reivindicação"""
        expected = f"Reivindicação de {self.usuario_reivindicador.username} para {self.item.titulo}"
        self.assertEqual(str(self.reivindicacao), expected)

class FormularioItemTest(TestCase):
    """
    Testes para o FormularioItem
    """
    
    def test_formulario_valido(self):
        """Testa formulário com dados válidos"""
        form_data = {
            'titulo': 'Carteira Perdida',
            'descricao': 'Carteira de couro marrom perdida na cantina com documentos importantes',
            'categoria': 'documentos',
            'tipo': 'perdido',
            'bloco': 'restaurante',
            'local_especifico': 'Mesa próxima à janela',
            'data_ocorrencia': timezone.now(),
            'telefone_contato': '(63) 99999-9999',
            'email_contato': 'test@uft.edu.br',
            'prioridade': True
        }
        
        form = FormularioItem(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_formulario_titulo_muito_curto(self):
        """Testa validação de título muito curto"""
        form_data = {
            'titulo': 'ABC',  # Muito curto
            'descricao': 'Descrição válida com mais de vinte caracteres para passar na validação',
            'categoria': 'outros',
            'tipo': 'perdido',
            'bloco': 'bloco_1'
        }
        
        form = FormularioItem(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors)
    
    def test_formulario_descricao_muito_curta(self):
        """Testa validação de descrição muito curta"""
        form_data = {
            'titulo': 'Título Válido',
            'descricao': 'Muito curta',  # Muito curta
            'categoria': 'outros',
            'tipo': 'perdido',
            'bloco': 'bloco_1'
        }
        
        form = FormularioItem(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('descricao', form.errors)

class ItemViewsTest(TestCase):
    """
    Testes para as views do sistema
    """
    
    def setUp(self):
        self.client = Client()
        self.usuario = User.objects.create_user(
            username='testuser',
            email='test@uft.edu.br',
            password='testpass123'
        )
        
        self.item = Item.objects.create(
            titulo='Item Teste',
            descricao='Descrição do item teste para visualização',
            categoria='outros',
            tipo='perdido',
            bloco='bloco_1',
            usuario=self.usuario
        )
    
    def test_listar_itens_view(self):
        """Testa a view de listagem de itens"""
        response = self.client.get(reverse('itens:listar-itens'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.titulo)
    
    def test_detalhe_item_view(self):
        """Testa a view de detalhes do item"""
        response = self.client.get(
            reverse('itens:detalhe-item', kwargs={'pk': self.item.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.titulo)
        self.assertContains(response, self.item.descricao)
    
    def test_criar_item_requer_login(self):
        """Testa que criar item requer login"""
        response = self.client.get(reverse('itens:criar-item'))
        self.assertEqual(response.status_code, 302)  # Redirect para login
    
    def test_criar_item_logado(self):
        """Testa criação de item com usuário logado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('itens:criar-item'))
        self.assertEqual(response.status_code, 200)
    
    def test_criar_item_post(self):
        """Testa POST para criar item"""
        self.client.login(username='testuser', password='testpass123')
        
        form_data = {
            'titulo': 'Novo Item Teste',
            'descricao': 'Descrição detalhada do novo item para teste de criação',
            'categoria': 'eletronicos',
            'tipo': 'encontrado',
            'bloco': 'biblioteca',
            'local_especifico': 'Sala de estudos',
            'data_ocorrencia': timezone.now(),
        }
        
        response = self.client.post(reverse('itens:criar-item'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect após sucesso
        
        # Verificar se item foi criado
        self.assertTrue(
            Item.objects.filter(titulo='Novo Item Teste').exists()
        )
    
    def test_editar_item_proprio_usuario(self):
        """Testa edição de item pelo próprio usuário"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('itens:editar-item', kwargs={'pk': self.item.pk})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_editar_item_usuario_diferente(self):
        """Testa que usuário não pode editar item de outro"""
        outro_usuario = User.objects.create_user(
            username='outro_user',
            password='pass123'
        )
        
        self.client.login(username='outro_user', password='pass123')
        response = self.client.get(
            reverse('itens:editar-item', kwargs={'pk': self.item.pk})
        )
        self.assertEqual(response.status_code, 404)  # Não encontrado
    
    def test_adicionar_comentario(self):
        """Testa adição de comentário"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('itens:adicionar-comentario', kwargs={'item_id': self.item.pk}),
            data={'texto': 'Este é um comentário de teste com texto suficiente'}
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(
            Comentario.objects.filter(
                item=self.item,
                usuario=self.usuario
            ).exists()
        )
    
    def test_meus_itens_view(self):
        """Testa a view de itens do usuário"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('itens:meus-itens'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.titulo)
    
    def test_filtros_busca(self):
        """Testa filtros de busca"""
        # Criar item com categoria específica
        item_eletronico = Item.objects.create(
            titulo='Notebook Dell',
            descricao='Notebook Dell Inspiron perdido na sala de aula',
            categoria='eletronicos',
            tipo='perdido',
            bloco='bloco_2',
            usuario=self.usuario
        )
        
        # Buscar por categoria
        response = self.client.get(
            reverse('itens:listar-itens') + '?categoria=eletronicos'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, item_eletronico.titulo)
        self.assertNotContains(response, self.item.titulo)  # Categoria diferente
    
    def test_api_itens_recentes(self):
        """Testa API de itens recentes"""
        response = self.client.get(reverse('itens:itens-recentes-api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        # Verificar se retorna JSON válido
        import json
        data = json.loads(response.content)
        self.assertIn('itens', data)
        self.assertIsInstance(data['itens'], list)

class IntegrationTest(TestCase):
    """
    Testes de integração do sistema
    """
    
    def setUp(self):
        self.client = Client()
        
        # Criar usuários
        self.usuario_perdeu = User.objects.create_user(
            username='perdeu_item',
            email='perdeu@uft.edu.br',
            password='pass123'
        )
        
        self.usuario_encontrou = User.objects.create_user(
            username='encontrou_item',
            email='encontrou@uft.edu.br',
            password='pass123'
        )
        
        # Item perdido
        self.item_perdido = Item.objects.create(
            titulo='Carteira Perdida',
            descricao='Carteira de couro marrom com documentos importantes',
            categoria='documentos',
            tipo='perdido',
            bloco='biblioteca',
            usuario=self.usuario_perdeu,
            prioridade=True
        )
        
        # Item encontrado
        self.item_encontrado = Item.objects.create(
            titulo='Carteira Encontrada',
            descricao='Carteira de couro marrom encontrada na biblioteca',
            categoria='documentos',
            tipo='encontrado',
            bloco='biblioteca',
            usuario=self.usuario_encontrou
        )
    
    def test_fluxo_completo_reivindicacao(self):
        """Testa fluxo completo de reivindicação de item"""
        # 1. Usuário que perdeu faz login
        self.client.login(username='perdeu_item', password='pass123')
        
        # 2. Visualiza item encontrado
        response = self.client.get(
            reverse('itens:detalhe-item', kwargs={'pk': self.item_encontrado.pk})
        )
        self.assertEqual(response.status_code, 200)
        
        # 3. Faz reivindicação
        response = self.client.post(
            reverse('itens:reivindicar-item', kwargs={'item_id': self.item_encontrado.pk}),
            data={'justificativa': 'Esta carteira é minha, tem meu RG e CPF dentro, perdi ontem na biblioteca'}
        )
        self.assertEqual(response.status_code, 302)
        
        # 4. Verificar se reivindicação foi criada
        reivindicacao = ReivindicacaoItem.objects.get(
            item=self.item_encontrado,
            usuario=self.usuario_perdeu
        )
        self.assertIsNotNone(reivindicacao)
        
        # 5. Usuário que encontrou faz login
        self.client.login(username='encontrou_item', password='pass123')
        
        # 6. Visualiza reivindicações recebidas
        response = self.client.get(reverse('itens:reivindicacoes-recebidas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reivindicacao.justificativa)
        
        # 7. Aprova a reivindicação
        response = self.client.post(
            reverse('itens:aprovar-reivindicacao', kwargs={'pk': reivindicacao.pk})
        )
        self.assertEqual(response.status_code, 302)
        
        # 8. Verificar se item foi marcado como resolvido
        self.item_encontrado.refresh_from_db()
        self.assertEqual(self.item_encontrado.status, 'resolvido')
        self.assertEqual(self.item_encontrado.resolvido_por, self.usuario_perdeu)
    
    def test_fluxo_comentarios(self):
        """Testa fluxo de comentários em item"""
        # Login do usuário
        self.client.login(username='encontrou_item', password='pass123')
        
        # Adicionar comentário
        response = self.client.post(
            reverse('itens:adicionar-comentario', kwargs={'item_id': self.item_perdido.pk}),
            data={'texto': 'Vi uma carteira similar no bloco 2, pode ser útil verificar lá também'}
        )
        self.assertEqual(response.status_code, 302)
        
        # Verificar se comentário aparece na página do item
        response = self.client.get(
            reverse('itens:detalhe-item', kwargs={'pk': self.item_perdido.pk})
        )
        self.assertContains(response, 'Vi uma carteira similar')
        
        # Verificar se comentário foi salvo no banco
        comentario = Comentario.objects.get(
            item=self.item_perdido,
            usuario=self.usuario_encontrou
        )
        self.assertIsNotNone(comentario)