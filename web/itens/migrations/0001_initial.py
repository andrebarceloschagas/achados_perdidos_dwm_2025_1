# Generated by Django 4.2.7 on 2025-06-01 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(help_text="Título descritivo do item (ex: 'Celular Samsung Galaxy')", max_length=200)),
                ('descricao', models.TextField(help_text='Descrição detalhada do item (cor, marca, características distintivas)', max_length=1000)),
                ('categoria', models.CharField(choices=[('eletronicos', 'Eletrônicos'), ('documentos', 'Documentos'), ('roupas_acessorios', 'Roupas e Acessórios'), ('livros_material', 'Livros e Material Escolar'), ('chaves', 'Chaves'), ('carteira_bolsa', 'Carteira/Bolsa'), ('joias_bijuterias', 'Joias e Bijuterias'), ('oculos', 'Óculos'), ('equipamentos_esportivos', 'Equipamentos Esportivos'), ('instrumentos_musicais', 'Instrumentos Musicais'), ('medicamentos', 'Medicamentos'), ('outros', 'Outros')], default='outros', help_text='Categoria do item para facilitar a busca', max_length=30)),
                ('tipo', models.CharField(choices=[('perdido', 'Item Perdido'), ('encontrado', 'Item Encontrado')], help_text='Tipo do registro: item perdido ou encontrado', max_length=10)),
                ('bloco', models.CharField(choices=[('bloco_1', 'Bloco 1 - Salas de Aula'), ('bloco_2', 'Bloco 2 - Laboratórios'), ('bloco_3', 'Bloco 3 - Administração'), ('bloco_4', 'Bloco 4 - Biblioteca'), ('bloco_5', 'Bloco 5 - Auditórios'), ('biblioteca', 'Biblioteca Central'), ('restaurante', 'Restaurante Universitário'), ('quadra_esportes', 'Quadra de Esportes'), ('ginasio', 'Ginásio Poliesportivo'), ('estacionamento', 'Estacionamento'), ('laboratorio_informatica', 'Laboratório de Informática'), ('laboratorio_ciencias', 'Laboratório de Ciências'), ('secretaria', 'Secretaria Acadêmica'), ('coordenacao', 'Coordenação de Curso'), ('diretoria', 'Diretoria do Campus'), ('cantina', 'Cantina'), ('area_convivencia', 'Área de Convivência'), ('jardim', 'Jardim/Área Verde'), ('portaria', 'Portaria'), ('outro', 'Outro Local')], help_text='Local onde o item foi perdido ou encontrado', max_length=30)),
                ('local_especifico', models.CharField(blank=True, help_text="Detalhes específicos do local (ex: 'Sala 101, 2º andar, próximo ao bebedouro')", max_length=200, null=True)),
                ('data_postagem', models.DateTimeField(auto_now_add=True, help_text='Data e hora em que o item foi cadastrado no sistema')),
                ('data_ocorrencia', models.DateTimeField(help_text='Data e hora aproximada em que o item foi perdido/encontrado')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, help_text='Última atualização do registro')),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('resolvido', 'Resolvido'), ('spam', 'Spam'), ('expirado', 'Expirado')], default='ativo', help_text='Status atual do item', max_length=10)),
                ('data_resolucao', models.DateTimeField(blank=True, help_text='Data em que o item foi devolvido/recuperado', null=True)),
                ('telefone_contato', models.CharField(blank=True, help_text='Telefone para contato (opcional)', max_length=20, null=True)),
                ('email_contato', models.EmailField(blank=True, help_text='Email para contato (opcional)', max_length=254, null=True)),
                ('visualizacoes', models.PositiveIntegerField(default=0, help_text='Número de visualizações do item')),
                ('prioridade', models.BooleanField(default=False, help_text='Marcar como prioritário (documentos importantes, medicamentos, etc.)')),
                ('resolvido_por', models.ForeignKey(blank=True, help_text='Usuário que ajudou a resolver o caso', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='itens_resolvidos', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(help_text='Usuário que cadastrou o item', on_delete=django.db.models.deletion.CASCADE, related_name='itens_postados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Itens',
                'ordering': ['-data_postagem'],
            },
        ),
        migrations.CreateModel(
            name='PontoEncontro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_encontro', models.CharField(help_text='Local específico para o encontro no campus', max_length=200)),
                ('data_encontro', models.DateTimeField(help_text='Data e hora agendada para o encontro')),
                ('observacoes', models.TextField(blank=True, help_text='Observações adicionais sobre o encontro', max_length=300, null=True)),
                ('confirmado_solicitante', models.BooleanField(default=False)),
                ('confirmado_postador', models.BooleanField(default=False)),
                ('realizado', models.BooleanField(default=False)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pontos_encontro', to='itens.item')),
                ('usuario_postador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encontros_agendados', to=settings.AUTH_USER_MODEL)),
                ('usuario_solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='encontros_solicitados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ponto de Encontro',
                'verbose_name_plural': 'Pontos de Encontro',
                'ordering': ['-data_encontro'],
            },
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(help_text='Comentário sobre o item (informações adicionais, dicas, etc.)', max_length=500)),
                ('data_comentario', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='itens.item')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comentário',
                'verbose_name_plural': 'Comentários',
                'ordering': ['data_comentario'],
            },
        ),
        migrations.CreateModel(
            name='Anuncio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('descricao', models.CharField(max_length=200)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anuncios_realizados', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Anúncio (Legado)',
                'verbose_name_plural': 'Anúncios (Legado)',
            },
        ),
        migrations.CreateModel(
            name='ReivindicacaoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('justificativa', models.TextField(help_text='Explique por que este item é seu (detalhes que comprovem a propriedade)', max_length=500)),
                ('data_reivindicacao', models.DateTimeField(auto_now_add=True)),
                ('aprovada', models.BooleanField(default=False)),
                ('data_resposta', models.DateTimeField(blank=True, null=True)),
                ('observacoes_admin', models.TextField(blank=True, help_text='Observações da administração sobre a reivindicação', max_length=300, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reivindicacoes', to='itens.item')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reivindicação de Item',
                'verbose_name_plural': 'Reivindicações de Itens',
                'ordering': ['-data_reivindicacao'],
                'unique_together': {('item', 'usuario')},
            },
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['tipo', 'status'], name='itens_item_tipo_ecaa8a_idx'),
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['categoria'], name='itens_item_categor_0cd1d0_idx'),
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['bloco'], name='itens_item_bloco_38e547_idx'),
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['-data_postagem'], name='itens_item_data_po_4018b4_idx'),
        ),
    ]
