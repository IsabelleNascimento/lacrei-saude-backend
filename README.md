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
   * Autenticação obrigatória via Token (DRF `TokenAuthentication`).
   * Estruturação de Logs ativos diretamente no console do servidor para monitoramento.

---

## 🚀 Como Executar o Projeto em Ambiente Local

Graças ao ambiente conteinerizado com Docker, você só precisa de alguns comandos para subir a infraestrutura completa do projeto.

### Pré-requisitos
* Git instalado
* Docker e Docker Compose instalados e em execução

### 1. Clonar o Repositório
```bash
git clone https://github.com/IsabelleNascimento/lacrei-saude-backend.git
cd lacrei-saude-backend
```

> **Nota:** Como o arquivo `.env` não é enviado ao GitHub por motivos de segurança, certifique-se de que ele esteja preenchido na raiz do seu projeto local (use o `.env.example` como base) antes de rodar os containers.

### 2. Executar o Docker Compose

Com o Docker aberto, execute o comando abaixo para construir as imagens e iniciar os containers da aplicação e do banco de dados:

```bash
docker compose up --build -d
```

A API estará disponível e respondendo em: `http://localhost:8000/`

### 3. Executar as Migrações e Criar Superusuário

Para estruturar o banco de dados e criar um acesso ao painel administrativo do Django, execute:

```bash
docker compose exec web python src/manage.py migrate
docker compose exec web python src/manage.py createsuperuser
```

---

## 🔐 Autenticação

A API utiliza autenticação via **Token (DRF `TokenAuthentication`)**. Todas as rotas exigem o header abaixo em cada requisição:

```
Authorization: Token <seu_token>
```

### Como obter um token

1. Crie um usuário (veja o passo 3 acima), ou use um que já exista.
2. Solicite o token informando usuário e senha:

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "seu_usuario", "password": "sua_senha"}'
```

Resposta esperada:
```json
{"token": "9f8a7b6c5d4e3f2a1b0c..."}
```

3. Use o token nas próximas requisições:

```bash
curl http://localhost:8000/api/profissionais/ \
  -H "Authorization: Token 9f8a7b6c5d4e3f2a1b0c..."
```

Requisições sem o header `Authorization` retornam `401 Unauthorized`.

---

## 🧪 Como Executar os Testes Automatizados

Os testes rodam de forma isolada dentro do container de aplicação, usando `APITestCase` do Django REST Framework. Para executar a suíte de testes:

```bash
docker compose exec web python src/manage.py test consultas
```

A cobertura atual inclui: listagem e criação de Profissionais, e validação de que o acesso sem token é bloqueado (`401`).

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
| **GET** | `/api/consultas/?profissional_id={id}` | **[Filtro Customizado]** Lista todas as consultas de um profissional específico. |
| **POST** | `/api/token/` | Autentica um usuário e retorna o token de acesso. |

> Todas as rotas acima (exceto `/api/token/`) exigem o header `Authorization: Token <token>`.

## 📄 Documentação Interativa

Com o projeto rodando localmente, acesse:
- Swagger UI: http://localhost:8000/api/docs/
- Redoc: http://localhost:8000/api/redoc/
---

## 🛠️ Detalhes de Implementação e Justificativas Técnicas

* **Segurança de Variáveis:** o projeto utiliza `python-dotenv` para carregar credenciais e chaves sensíveis a partir de um arquivo `.env`, nunca expostas diretamente no código-fonte. O `.env.example` documenta as variáveis necessárias sem expor valores reais.
* **Autenticação por Token (DRF):** optei pelo `TokenAuthentication` nativo do Django REST Framework em vez de JWT por ser mais simples de configurar e suficiente para o escopo do desafio (controle básico de acesso à API), evitando a complexidade adicional de refresh tokens que o JWT normalmente traz. Para um cenário de produção com múltiplos serviços/clientes, JWT seria a evolução natural.
* **Políticas de CORS:** configuradas via `django-cors-headers`, permitindo integração segura com aplicações Frontend que consumirão essa API futuramente.
* **Poetry + Docker:** a escolha do Poetry para gerenciamento de dependências garante builds reprodutíveis através do `poetry.lock`, versionado junto ao `pyproject.toml`. O Dockerfile copia ambos os arquivos antes de instalar as dependências, garantindo que o ambiente do container sempre resolva exatamente as mesmas versões testadas localmente.
* **Estrutura de pastas (`src/`):** o código Django fica isolado em `src/`, separando claramente o código da aplicação dos arquivos de configuração de infraestrutura (Docker, CI, Poetry) que ficam na raiz do repositório.
* **Integração Contínua (CI):** este repositório conta com uma esteira automatizada via **GitHub Actions**, que builda a aplicação via Docker Compose, roda as migrações e executa os testes automatizados a cada *push* ou *pull request* na branch `main`, garantindo que nenhuma alteração quebre o funcionamento existente antes de ser mesclada.

---

## 🔄 Proposta de Rollback

A estratégia de rollback deste projeto é organizada em camadas, da mais rápida/simples para a mais robusta, dependendo da gravidade da falha identificada após um deploy.

### 1. Rollback rápido via revert de commit (camada imediata)

Se um problema for identificado logo após o merge na branch `main`, a forma mais rápida de reverter é desfazer o commit problemático e deixar o próprio pipeline de CI/CD reconstruir e reimplantar a versão anterior automaticamente:

```bash
git revert <hash-do-commit-problematico>
git push origin main
```

Isso dispara o workflow do GitHub Actions normalmente (lint → build/test → deploy), publicando a versão anterior sem intervenção manual em infraestrutura.

**Quando usar:** falhas identificadas minutos após o deploy, com causa raiz clara no último commit.

### 2. Rollback via imagem Docker versionada (camada de infraestrutura)

Cada deploy realizado pelo pipeline gera uma imagem Docker taggeada com o hash curto do commit (ex: `lacrei-backend:a1b2c3d`), publicada em um registry (Amazon ECR). Isso significa que toda versão já implantada continua disponível e pronta para reuso.

Em caso de falha que não possa esperar um novo ciclo de CI/CD, o rollback consiste em reimplantar diretamente a última imagem estável, sem rebuildar:

```bash
# Exemplo de rollback manual via AWS CLI, apontando o serviço para a imagem anterior
aws ecs update-service \
  --cluster lacrei-saude-cluster \
  --service lacrei-saude-backend \
  --task-definition lacrei-saude-backend:<revisao-estavel-anterior> \
  --force-new-deployment
```

**Quando usar:** falhas críticas em produção, quando cada minuto de indisponibilidade importa e não há tempo de esperar um novo build completo.

### 3. Rollback de migrações de banco de dados

Rollback de código nem sempre é compatível com migrações de banco já aplicadas. Por isso, toda migração que não for puramente aditiva (ex: remoção de coluna, alteração de tipo) deve ser escrita de forma reversível, com `reverse_code` definido:

```python
def reverse_func(apps, schema_editor):
    # lógica para desfazer a alteração
    ...

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(forward_func, reverse_func),
    ]
```

Para reverter uma migração específica já aplicada:

```bash
docker compose exec web python src/manage.py migrate consultas <nome_da_migracao_anterior>
```

**Quando usar:** sempre que o rollback de código envolver reverter também uma alteração de schema do banco.

### 4. Evolução futura: Deploy Blue/Green

Para eliminar downtime durante o rollback, a evolução natural seria manter dois ambientes espelhados (blue/green) atrás de um load balancer, alternando o tráfego entre eles. Um rollback se tornaria apenas uma troca de roteamento — instantânea, sem precisar reimplantar nada. Essa abordagem não foi implementada nesta entrega por limitação de tempo, mas é a próxima evolução natural da estratégia de deploy deste projeto.

### Resumo de decisão

| Cenário | Estratégia recomendada |
| --- | --- |
| Bug identificado minutos após o merge | Revert de commit (camada 1) |
| Indisponibilidade crítica em produção | Reimplantar imagem anterior (camada 2) |
| Rollback envolve mudança de schema no banco | Migração reversível (camada 3) |
| Necessidade de rollback sem downtime | Blue/Green (evolução futura) |
---

## 📌 Erros Encontrados e Melhorias Futuras

* Corrigido: incompatibilidade entre `pyproject.toml` e `poetry.lock` que quebrava o build do Docker após adicionar novas dependências — resolvido com `poetry lock` e ajuste do `Dockerfile` para copiar o `poetry.lock` junto ao `pyproject.toml`.
* Corrigido: endpoint de filtro de consultas por profissional documentado incorretamente como rota aninhada; ajustado para refletir a implementação real via query param (`?profissional_id=`).
* Pendente: ampliar cobertura de testes automatizados para o CRUD completo de Consultas e casos de erro (dados ausentes/inválidos).
* Pendente: configurar logging estruturado (arquivo de log ou serviço externo) além do output padrão do console.
* Pendente: adicionar etapas de Lint e Deploy ao pipeline de CI/CD.
* Pendente: deploy funcional em ambientes de staging e produção na AWS.
