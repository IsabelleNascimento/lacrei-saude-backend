```markdown
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

Graças ao ambiente conteinerizado com Docker, você só precisa de alguns comandos para subir a infraestrutura completa do projeto.

### Pré-requisitos
* Git instalado
* Docker e Docker Compose instalados e em execução

### 1. Clonar o Repositório
```bash
git clone [https://github.com/seu-usuario/lacrei-saude-backend.git](https://github.com/seu-usuario/lacrei-saude-backend.git)
cd lacrei-saude-backend

```

> **Nota:** Como o arquivo `.env` não é enviado ao GitHub por motivos de segurança, certifique-se de que ele esteja preenchido na raiz do seu projeto local antes de rodar os containers.

### 2. Executar o Docker Compose

Com o Docker aberto, execute o comando abaixo para construir as imagens e iniciar os containers da aplicação e do banco de dados:

```bash
docker compose up --build

```

A API estará disponível e respondendo em: `http://localhost:8000/`

### 3. Executar as Migrações e Criar Superusuário (Opcional)

Para estruturar o banco de dados e criar um acesso ao painel administrativo do Django, execute em outro terminal:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser

```

---

## 🧪 Como Executar os Testes Automatizados

Os testes rodam de forma isolada dentro do container de aplicação. Para executar a suíte de testes e validar os endpoints, utilize:

```bash
docker compose exec web python manage.py test

```

---

## 🎯 Documentação da API (Endpoints)

| Método | Endpoint | Descrição |
| --- | --- | --- |
| **GET** | `/api/profissionais/` | Lista todos os profissionais de saúde cadastrados. |
| **POST** | `/api/profissionais/` | Cadastra um novo profissional de saúde. |
| **GET** | `/api/profissionais/{id}/` | Retorna os detalhes de um profissional específico. |
| **PUT** | `/api/profissionais/{id}/` | Atualiza completamente os dados de um profissional. |
| **DELETE** | `/api/profissionais/{id}/` | Remove um profissional do sistema. |
| **GET** | `/api/consultas/` | Lista todos os agendamentos de consultas. |
| **POST** | `/api/consultas/` | Cria um novo agendamento de consulta. |
| **GET** | `/api/profissionais/{id}/consultas/` | **[Filtro Customizado]** Lista todas as consultas de um profissional específico. |

---

## 🛠️ Detalhes de Implementação e Segurança

* **Segurança de Variáveis:** O projeto utiliza `python-dotenv` para garantir que nenhuma credencial sensível ou chave de criptografia fique exposta no código-fonte.
* **Políticas de CORS:** Configurado através do `django-cors-headers` para permitir a integração segura com aplicações Frontend.
* **Integração Contínua (CI):** Este repositório conta com uma esteira automatizada via **GitHub Actions** que executa os testes a cada *push* ou *pull request* na branch `main`, garantindo a estabilidade e integridade do código antes de qualquer deploy.

```
