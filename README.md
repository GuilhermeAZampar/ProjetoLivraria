# 📚 Projeto Livraria — FastAPI + React

Aplicação Full Stack para gerenciamento de livros, desenvolvida com FastAPI no back-end e React + Vite no front-end.

O projeto começou como uma API REST para gerenciamento de livros e evoluiu para uma aplicação Full Stack, incluindo interface web, autenticação HTTP Basic, persistência de dados, cache com Redis, tarefas assíncronas, mensageria, testes automatizados e containerização.

## 🚀 Tecnologias utilizadas

### Back-end
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Redis
- Celery
- Kafka
- Elasticsearch
- Pytest
- Docker
- Kubernetes

### Front-end
- React
- JavaScript
- Vite
- HTML5
- CSS3
- Fetch API

### DevOps e ferramentas
- Git
- GitHub
- GitHub Actions
- Docker
- Kubernetes
- Poetry

## 📌 Funcionalidades

A aplicação permite:

- Listar livros cadastrados
- Cadastrar novos livros
- Editar livros existentes
- Excluir livros
- Paginar os resultados da API
- Autenticar requisições utilizando HTTP Basic
- Validar dados enviados pelo usuário
- Exibir mensagens de sucesso e erro
- Confirmar exclusões através de modal
- Utilizar interface responsiva para desktop e dispositivos móveis

## ⚙️ Back-end

O back-end foi desenvolvido utilizando FastAPI e disponibiliza uma API REST para gerenciamento dos livros.

Principais endpoints:

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/livros` | Lista os livros |
| POST | `/adicionar` | Cadastra um novo livro |
| PUT | `/atualizar/{id_livro}` | Atualiza um livro |
| DELETE | `/deletar/{id_livro}` | Exclui um livro |
| POST | `/calcular/soma` | Envia uma tarefa de soma |
| POST | `/calcular/fatorial` | Envia uma tarefa de fatorial |
| GET | `/tarefas/resultado` | Consulta resultados das tarefas |
| GET | `/debug/redis` | Consulta informações armazenadas no Redis |
| GET | `/chamadas-externa` | Demonstra execução assíncrona |

A documentação interativa da API pode ser acessada através do Swagger:

```text
http://127.0.0.1:8000/docs
```

## ⚛️ Front-end

O front-end foi desenvolvido com React e Vite e consome diretamente os endpoints disponibilizados pelo FastAPI.

A interface possui:

- Formulário controlado para cadastro e edição
- Listagem dos livros em cards
- Atualização automática após operações CRUD
- Modal de confirmação para exclusões
- Validação de formulários
- Tratamento de erros da API
- Mensagens de sucesso e erro
- Layout responsivo

## 🔴 Redis

O Redis é utilizado como sistema de cache.

Foi implementada uma flag de configuração para permitir que a aplicação funcione mesmo quando o Redis não estiver disponível.

No arquivo `.env`:

```env
USE_REDIS=false
```

Para utilizar o Redis:

```env
USE_REDIS=true
```

Quando desativado, a aplicação consulta diretamente o banco de dados sem tentar estabelecer conexão com o Redis.

## ⚡ Celery

O Celery é utilizado para processamento de tarefas em segundo plano.

O projeto possui exemplos de tarefas assíncronas para:

- Soma de valores
- Cálculo de fatorial

Os IDs das tarefas podem ser armazenados no Redis e posteriormente utilizados para consultar seus resultados.

## 📨 Kafka

O projeto utiliza Kafka para publicação de eventos relacionados às operações realizadas na aplicação.

Por exemplo, ao cadastrar um livro, um evento pode ser enviado para o tópico:

```text
livros_eventos
```

Isso demonstra o uso de mensageria e arquitetura orientada a eventos.

## 🗄️ Banco de dados

A aplicação utiliza SQLAlchemy como ORM.

Durante o desenvolvimento local, pode ser utilizado SQLite.

O arquivo do banco local não é versionado no GitHub.

## 🔐 Variáveis de ambiente

As configurações sensíveis são armazenadas em um arquivo `.env`, que não é versionado pelo Git.

Exemplo de configuração:

```env
DATABASE_URL=sqlite:///./livros.db

meu_usuario=seu_usuario
minha_senha=sua_senha

REDIS_HOST=localhost
REDIS_PORT=6379
USE_REDIS=false

ELASTICSEARCH_URL=http://localhost:9200
ELASTICSEARCH_INDEX=livros-logs
```

> Nunca envie seu arquivo `.env` com credenciais reais para o repositório.

## ▶️ Executando o back-end

Instale as dependências utilizando Poetry:

```bash
poetry install
```

Inicie a API:

```bash
poetry run uvicorn main:app --reload
```

O servidor será disponibilizado em:

```text
http://127.0.0.1:8000
```

## ▶️ Executando o front-end

Entre na pasta do front-end:

```bash
cd frontend
```

Instale as dependências:

```bash
npm install
```

Inicie o Vite:

```bash
npm run dev
```

A aplicação estará disponível normalmente em:

```text
http://localhost:5173
```

## 🧪 Testes

O projeto utiliza Pytest para testes automatizados do back-end.

Para executar:

```bash
poetry run pytest
```

Os testes também fazem parte do fluxo de integração contínua através do GitHub Actions.

## 🔄 CI/CD

O projeto possui workflow configurado no GitHub Actions para executar verificações automaticamente durante alterações no repositório e Pull Requests.

Dessa forma, alterações podem ser verificadas antes de serem incorporadas à branch principal.

## 📂 Estrutura simplificada

```text
MainBackEnd/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── LivroCard.jsx
│   │   │   └── LivroForm.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── tests/
├── main.py
├── tasks.py
├── celery_app.py
├── kafka_producer.py
├── docker-compose.yml
├── Dockerfile
├── deployment.yaml
├── service.yaml
├── pyproject.toml
└── README.md
```

## 📈 Evolução do projeto

Este projeto foi desenvolvido inicialmente como uma API back-end e posteriormente evoluído para uma aplicação Full Stack.

Durante seu desenvolvimento foram aplicados conceitos como:

- Desenvolvimento de APIs REST
- CRUD
- Integração entre front-end e back-end
- ORM e persistência de dados
- Autenticação
- Cache
- Processamento assíncrono
- Mensageria
- Logs
- Containerização
- Testes automatizados
- CI/CD
- Responsividade
- Tratamento de erros

## 👨‍💻 Autor

Guilherme Zampar

Desenvolvedor Full Stack Python em formação, com foco em desenvolvimento Back-end.

GitHub: GuilhermeAZampar
