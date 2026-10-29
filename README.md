#Projeto Livraria

Aplicação full stack que desenvolvi para organizar um catálogo de livros, permitindo cadastrar, consultar, editar e excluir registros em uma interface responsiva.

Comecei pela API com Python e FastAPI e depois criei a interface com React e Vite. Implementei autenticação HTTP Basic, paginação, validação de dados, cache com Redis e eventos com Kafka. Também adicionei exemplos de tarefas em segundo plano com Celery.

Utilizei SQLAlchemy e SQLite para persistência, Elasticsearch para logs, Pytest para testes e GitHub Actions para verificações automáticas. O projeto inclui configuração para Docker e Kubernetes.

Para testar localmente, configure o `.env` e execute o back-end:

```bash
poetry install
poetry run uvicorn main:app --reload
```

Em outro terminal, inicie o front-end:

```bash
cd frontend
npm install
npm run dev
```

Acesse a interface em http://localhost:5173 e a documentação da API em http://127.0.0.1:8000/docs.

Para executar os testes:

```bash
poetry run pytest
```

Desenvolvido por [Guilherme Zampar](https://github.com/GuilhermeAZampar).
