# Sistema de Achados & Perdidos - UFT/Palmas

<div align="center">
  <img src="mobile/src/assets/logo-uft.png" alt="Logo UFT" width="200">
</div>

Sistema para gerenciar itens perdidos e encontrados na Universidade Federal do Tocantins (UFT) - Campus Palmas. O projeto consiste em uma aplicação web concebido em Django e um aplicativo mobile com Ionic/Angular.

Projeto desenvolvido como parte da disciplina de Desenvolvimento Web e Mobile (DWM) do curso de Ciência da Computação/UFT.

Desenvolvidido por: **[Antonio André Barcelos Chagas](https://github.com/andrebarceloschagas)**

Sob a supervisão do professor **Thiago Magalhães**

## Sobre o Projeto

O sistema permite que estudantes, professores e funcionários da UFT possam:

- **Cadastrar itens perdidos**: Registrar objetos que foram perdidos no campus
- **Cadastrar itens encontrados**: Registrar objetos que foram encontrados
- **Buscar itens**: Pesquisar por itens usando filtros avançados
- **Reivindicar itens**: Solicitar a devolução de itens encontrados
- **Acompanhar status**: Verificar se os itens foram devolvidos ou encontrados

### Aplicação Web (Django)

- **Gestão administrativa**: Interface para administração de itens, usuários e configurações
- **API REST**: Backend que fornece endpoints para o aplicativo mobile
- **Dashboard Admin**: Interface completa para gerenciamento do sistema

### Aplicativo Mobile (Ionic/Angular)

- **Interface amigável**: Design intuitivo e responsivo para uso em smartphones
- **Cadastro de itens**: Registro simplificado de itens com upload de fotos
- **Navegação por categorias**: Organização dos itens por tipo, local e categoria
- **Notificações**: Alertas sobre itens encontrados similares aos cadastrados

## Tecnologias Utilizadas

### Web
- **Framework**: Django
- **API**: Django REST Framework
- **Banco de Dados**: SQLite
- **Autenticação**: JWT (JSON Web Tokens)
- **Frontend Web**: Bootstrap 5

### Mobile
- **Framework**: Ionic com Angular
- **UI Components**: Ionic UI
- **Autenticação**: JWT integrado
- **Armazenamento**: Ionic Storage



## Principais Funcionalidades

### Aplicação Web
- Painel administrativo completo
- Gerenciamento de usuários
- Moderação de itens e comentários
- API REST para comunicação com o app mobile
- Relatórios e estatísticas

### Aplicativo Mobile
- Cadastro de itens perdidos/encontrados com fotos
- Exclusão de itens cadastrados
- Edição de itens cadastrados
- Filtros por tipo de item (perdido/encontrado)
- Visualização detalhada de itens
