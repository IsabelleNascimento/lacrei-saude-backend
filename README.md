# Lacrei Saúde - Desafio Técnico Backend 🚀

Este repositório contém o desenvolvimento de uma API REST completa para o gerenciamento de profissionais de saúde e agendamento de consultas, criada como parte do processo seletivo da Lacrei Saúde.

A aplicação foi desenvolvida seguindo boas práticas de arquitetura de software, isolamento de ambiente, segurança de dados e testes automatizados.

## 🛠️ Tecnologias e Ferramentas Utilizadas

* **Linguagem:** Python 3.13
* **Framework:** Django 6.0 + Django REST Framework (DRF)
* **Gerenciador de Dependências:** Poetry
* **Banco de Dados:** PostgreSQL 15
* **Conteinerização:** Docker & Docker Compose
* **Qualidade de Código:** Testes automatizados integrados (`APITestCase`)

## 🏗️ Arquitetura e Recursos Implementados

1. **CRUD Completo:** Endpoints robustos para cadastro, listagem, atualização e remoção de Profissionais e Consultas.
2. **Filtros Personalizados:** Endpoint customizado para listagem de consultas associadas a um profissional específico através do ID.
3. **Isolamento com Docker:** Configuração multi-container separando a aplicação do banco de dados relacional.
4. **Segurança e Boas Práticas:**
   * Centralização de credenciais e chaves por variáveis de ambiente (`.env`).
   * Configuração de segurança de acessos via CORS (`django-cors-headers`).
   * Estruturação de Logs ativos diretamente no console do servidor para monitoramento.

---

## 🚀 Como Executar o Projeto em Ambiente Local

Graças ao ambiente conteinerizado com Docker, você só precisa de um comando para subir a infraestrutura completa do projeto.

### Pré-requisitos
* Git instalado
* Docker e Docker Compose instalados e em execução

### 1. Clonar o Repositório
```bash
git clone [https://github.com/seu-usuario/lacrei-saude-backend.git](https://github.com/seu-usuario/lacrei-saude-backend.git)
cd lacrei-saude-backend