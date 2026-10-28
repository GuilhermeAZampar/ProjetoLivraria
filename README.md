Projeto Livraria

Comecei este projeto como uma API para gerenciar livros e depois desenvolvi uma interface com React e Vite. A aplicação permite cadastrar, listar, editar e excluir livros, com paginação, validação dos dados e autenticação HTTP Basic.

Na interface, é possível cadastrar e editar livros por formulário, visualizar os registros em cards e confirmar exclusões por um modal. O layout se adapta a computadores e celulares e exibe mensagens com o resultado das operações.

O back-end foi desenvolvido com Python e FastAPI, utilizando SQLAlchemy para acessar o banco de dados e SQLite no ambiente local. Também implementei cache com Redis, que pode ser ativado ou desativado pela configuração, tarefas em segundo plano com Celery e publicação de eventos com Kafka. As tarefas de soma e fatorial servem como exemplos de processamento em segundo plano.

O projeto também utiliza Elasticsearch para logs, Pytest nos testes automatizados e GitHub Actions para executar verificações nas alterações do repositório. A estrutura inclui arquivos para execução com Docker e configuração para Kubernetes.

Para executar o back-end, configure o arquivo .env com a conexão do banco, as credenciais de autenticação e as configurações dos serviços utilizados. Depois, instale as dependências e inicie a API:

poetry install
poetry run uvicorn main:app --reload

A API ficará disponível em http://127.0.0.1:8000 e a documentação interativa em http://127.0.0.1:8000/docs.

Para executar o front-end, abra outro terminal e rode:

cd frontend
npm install
npm run dev

A interface ficará disponível, por padrão, em http://localhost:5173.

Para executar os testes do back-end:

poetry run pytest

Desenvolvido por Guilherme Zampar.
