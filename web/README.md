# Sistema de Achados & Perdidos WEB - UFT/Palmas

Sistema web desenvolvido em Django para gerenciar itens perdidos e encontrados no campus da Universidade Federal do Tocantins (UFT) - Campus Palmas. 

## Sobre o Projeto

O sistema permite que estudantes, professores e funcionários da UFT possam:

- **Cadastrar itens perdidos**: Registrar objetos que foram perdidos no campus
- **Cadastrar itens encontrados**: Registrar objetos que foram encontrados
- **Buscar itens**: Pesquisar por itens usando filtros avançados
- **Reivindicar itens**: Solicitar a devolução de itens encontrados
- **Comentar**: Adicionar informações úteis sobre os itens
- **Agendar encontros**: Marcar locais e horários para devolução

## Funcionalidades

### Para Usuários
- Cadastro e autenticação de usuários
- Cadastro de itens perdidos/encontrados
- Sistema de busca com filtros avançados
- Visualização detalhada de itens
- Sistema de comentários
- Reivindicação de itens encontrados
- Agendamento de pontos de encontro
- Painel pessoal com histórico de itens
- Notificações de reivindicações

### Para Administradores
- Painel administrativo completo
- Moderação de itens e comentários
- Aprovação/rejeição de reivindicações
- Relatórios e estatísticas
- Gerenciamento de usuários

## Tecnologias Utilizadas
- WEB
    - **Backend**: Django
    - **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
    - **Banco de Dados**: SQLite
    - **Autenticação**: Django Auth

## Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- pip
- virtualenv

### Passo a passo

1. **Clone o repositório**
```bash
git clone https://github.com/andrebarceloschagas/achados_perdidos_dwm_2025_1.git
cd web
```

2. **Crie e ative um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute o servidor de desenvolvimento**
```bash
python manage.py runserver
```

O sistema estará disponível em `http://localhost:8000`

## Estrutura do Projeto WEB

```
achados_perdidos_uft/
├── achados_perdidos_uft/     # Configurações principais do projeto
│   ├── __init__.py
│   ├── settings.py           # Configurações do Django
│   ├── urls.py              # URLs principais
│   ├── wsgi.py              # Configuração WSGI
│   ├── asgi.py              # Configuração ASGI
│   ├── bibliotecas.py       # Funções auxiliares
│   ├── views.py             # Views gerais
│   └── static/              # Arquivos estáticos
├── itens/                   # App principal (achados e perdidos)
│   ├── models.py            # Modelos de dados
│   ├── views.py             # Views do app
│   ├── forms.py             # Formulários
│   ├── urls.py              # URLs do app
│   ├── admin.py             # Configuração do admin
│   ├── tests.py             # Testes
│   └── migrations/          # Migrações do banco
├── templates/               # Templates HTML
├── static/                  # Arquivos estáticos globais
├── media/                   # Uploads de usuários
├── manage.py               # Script de gerenciamento
├── requirements.txt        # Dependências
└── README.md              # Este arquivo
```

## 🎯 Modelos de Dados

### Item
- Título, descrição, categoria
- Tipo (perdido/encontrado)
- Local (bloco, local específico)
- Data da ocorrência
- Status (ativo, resolvido, spam)
- Prioridade, visualizações
- Contatos (telefone, email)

### Comentário
- Texto do comentário
- Usuário, item, data

### Reivindicação
- Justificativa
- Status de aprovação
- Datas de criação e resposta

### Ponto de Encontro
- Local e data do encontro
- Confirmações dos usuários
- Status de realização

## 🔧 Configuração de Produção

### Variáveis de Ambiente (.env)
```env
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
DATABASE_URL=postgres://user:pass@localhost/dbname
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-app
```

### Deploy com Gunicorn
```bash
gunicorn achados_perdidos_uft.wsgi:application --bind 0.0.0.0:8000
```

## 🧪 Testes

Execute os testes com:
```bash
python manage.py test
```

Para relatório de cobertura:
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # Gera relatório HTML
```

## 📊 Comandos Úteis

### Criar dados de exemplo
```bash
python manage.py shell
# Execute o script de dados de exemplo
```

### Backup do banco de dados
```bash
python manage.py dumpdata > backup.json
```

### Restaurar backup
```bash
python manage.py loaddata backup.json
```

### Limpar cache
```bash
python manage.py clear_cache
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Equipe de Desenvolvimento

- **Desenvolvedor Principal**: [Seu Nome]
- **Orientador**: [Nome do Orientador]
- **Instituição**: Universidade Federal do Tocantins - Campus Palmas

## 📞 Contato

- **Email**: contato@uft.edu.br
- **Site**: https://www.uft.edu.br
- **Campus**: UFT Palmas - Quadra 109 Norte, Avenida NS-15, ALCNO-14

## 🔄 Changelog

### v2.0.0 (Atual)
- ✅ Reestruturação completa do projeto
- ✅ Novo sistema de achados e perdidos
- ✅ Interface moderna com Bootstrap 5
- ✅ Sistema de reivindicações
- ✅ Pontos de encontro
- ✅ Filtros avançados de busca
- ✅ Painel administrativo melhorado
- ✅ Testes automatizados
- ✅ Documentação completa

### v1.0.0 (Legado)
- Sistema básico de anúncios
- Funcionalidades limitadas

## 🎯 Roadmap

### Próximas Funcionalidades
- [ ] Sistema de notificações por email
- [ ] App mobile (React Native)
- [ ] API REST completa
- [ ] Sistema de chat em tempo real
- [ ] Integração com redes sociais
- [ ] Geolocalização de itens
- [ ] Sistema de reputação de usuários
- [ ] Relatórios avançados
- [ ] Backup automático
- [ ] Múltiplos idiomas

## 🏆 Reconhecimentos

- Universidade Federal do Tocantins
- Comunidade Django Brasil
- Bootstrap Team
- Todos os contribuidores do projeto

---

**Sistema de Achados & Perdidos UFT Palmas** - Conectando pessoas aos seus pertences perdidos! 🎓📱💼