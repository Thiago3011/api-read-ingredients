# Allergy Validator

API para identificação de possíveis componentes alergênicos em listas de ingredientes, com autenticação, dados individualizados por usuário e extração de texto de imagens por OCR.

O Allergy Validator é uma aplicação web desenvolvida para ajudar o usuário a comparar ingredientes informados manualmente ou extraídos de rótulos com a lista de alergias que ele próprio cadastrou.

> **Aviso:** esta aplicação é uma ferramenta auxiliar. Ela não substitui orientação médica, a leitura cuidadosa do rótulo ou a confirmação de informações com o fabricante. OCR e correspondência de texto podem deixar de identificar ingredientes ou produzir resultados incorretos.

## Funcionalidades

- Cadastro de usuários e login.
- Autenticação baseada em JWT.
- Armazenamento de senhas por hash.
- Endpoints protegidos para usuários autenticados.
- Consulta de perfil limitada ao usuário autenticado.
- Cadastro, listagem e exclusão das próprias alergias.
- Isolamento de alergias entre usuários.
- Validação por texto, imagem ou texto e imagem na mesma requisição.
- Extração de texto de imagens com Tesseract OCR.
- Respostas de erro HTTP para falhas de processamento de imagem.
- Interface web para login, gerenciamento de alergias e validação.
- Testes automatizados com Pytest.
- Execução em containers com Docker Compose.

## Tecnologias

| Tecnologia | Utilização |
|---|---|
| Python 3.12 | Linguagem do backend |
| FastAPI | API REST e documentação OpenAPI |
| SQLAlchemy | ORM e acesso ao banco |
| PostgreSQL | Banco de dados |
| Pydantic / pydantic-settings | Validação de dados e configurações |
| Alembic | Migrações versionadas do banco de dados |
| JWT (python-jose) | Tokens de autenticação |
| pwdlib / Argon2 | Hash de senhas |
| Tesseract OCR / Pytesseract | Extração de texto de imagens |
| Pillow / Pillow-Heif | Processamento e leitura de imagens |
| HTML, CSS e JavaScript | Frontend |
| Docker / Docker Compose | Containerização e execução local |
| Pytest | Testes automatizados |

## Arquitetura

O backend separa responsabilidades entre routers, services, repositories e models.

```text
Cliente web
    |
    v
Router (FastAPI)
    |
    v
Service (regras de negócio)
    |
    v
Repository (acesso a dados)
    |
    v
PostgreSQL
```

- **Routers:** recebem as requisições HTTP, declaram dependências e retornam respostas.
- **Services:** implementam as regras de negócio.
- **Repositories:** concentram operações de consulta e persistência.
- **Models:** representam as entidades persistidas via SQLAlchemy.
- **Schemas:** definem e validam estruturas de entrada e saída.
- **Core:** reúne configurações e dependências compartilhadas, incluindo autenticação.

### Modelo de alergias

Cada alergia pertence diretamente ao usuário que a cadastrou:

```text
User
 └── Allergy
      ├── id
      ├── name
      └── user_id
```

As operações de listar, validar e excluir alergias levam em conta o usuário autenticado. Não há necessidade de uma lista global compartilhada.

## Executar localmente com Docker

### Pré-requisitos

- Git
- Docker Desktop com Docker Compose

Clone o repositório:

```bash
git clone https://github.com/Thiago3011/api-read-ingredients.git
cd api-read-ingredients
```

Crie um `.env` a partir do modelo e troque `JWT_SECRET_KEY` por um valor aleatório. No PowerShell, execute `Copy-Item .env.example .env` somente se ainda não existir um `.env`; não sobrescreva a configuração de um ambiente em uso. O `.env` não deve ser enviado ao Git.

O `docker-compose.yml` é destinado ao desenvolvimento local: publica a API e o PostgreSQL somente em `127.0.0.1`, aguarda o healthcheck do banco e ativa `--reload` apenas nesse ambiente. As credenciais padrão são locais e não devem ser reutilizadas em produção. Se o volume `postgres_data` já existe, mantenha os valores `POSTGRES_USER`, `POSTGRES_PASSWORD` e `POSTGRES_DB` compatíveis com a inicialização original do banco; mudar essas variáveis não altera automaticamente um usuário já criado no PostgreSQL.

Inicie os serviços:

```bash
docker compose up -d --build
```

Confira o estado e os logs:

```bash
docker compose ps
docker compose logs -f api
```

### Preparar o banco com Alembic

Em um banco novo, aplique a migração inicial depois que os containers estiverem em execução:

```bash
docker compose exec api alembic upgrade head
```

Se estiver atualizando um banco local antigo que já possui as tabelas `users` e `allergies`, primeiro confirme que o esquema corresponde à migração inicial. Para o banco existente deste projeto, esse esquema foi conferido. Registre a revisão atual **uma única vez**, sem recriar tabelas nem apagar dados:

```bash
docker compose exec api alembic stamp head
```

Depois disso, `docker compose exec api alembic upgrade head` aplica as futuras migrações pendentes. `python init_db.py` executa o mesmo comando de atualização via Alembic. Não use `alembic stamp head` num banco novo.

Acesse a aplicação em [http://localhost:8000](http://localhost:8000) e o Swagger em [http://localhost:8000/docs](http://localhost:8000/docs). Para parar os containers, execute `docker compose down`. O volume nomeado `postgres_data` preserva os dados; não use `docker compose down -v` se quiser mantê-los.

## Executar localmente sem container da API

O PostgreSQL e o Tesseract precisam estar disponíveis no ambiente. Crie e ative um ambiente virtual e instale as dependências:

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure as variáveis de ambiente em `.env`, apontando `DATABASE_URL` para o PostgreSQL acessível pela máquina e configurando `TESSERACT_CMD` caso o executável não esteja no PATH. Em seguida, inicie a aplicação:

```bash
uvicorn app.main:app --reload
```

A aplicação estará disponível em [http://localhost:8000](http://localhost:8000).

## Principais endpoints

Os endpoints abaixo refletem os routers atuais do projeto.

| Método | Endpoint | Descrição | Autenticação |
|---|---|---|---|
| POST | `/user/` | Criar usuário | Não |
| GET | `/user/me` | Consultar o próprio perfil | JWT |
| GET | `/user/{user_id}` | Consultar usuário | JWT |
| PATCH | `/user/{user_id}` | Atualizar o próprio usuário | JWT; apenas o próprio usuário |
| DELETE | `/user/{user_id}` | Excluir o próprio usuário | JWT; apenas o próprio usuário |
| POST | `/auth/login` | Entrar e obter token | Não |
| GET | `/user/allergies/` | Listar as próprias alergias | JWT |
| POST | `/user/allergies/?name={nome}` | Cadastrar alergia | JWT |
| DELETE | `/user/allergies/{allergy_id}` | Excluir uma alergia própria | JWT |
| POST | `/validation/` | Validar ingredientes com texto e/ou imagem | JWT |
| GET | `/health` | Verificar disponibilidade da API e do banco | Não |

Para endpoints protegidos, envie o token no cabeçalho:

```http
Authorization: Bearer <seu_token>
```

### Login

O endpoint `POST /auth/login` recebe JSON com `email` e `password`. Consulte o Swagger para verificar o formato exato da resposta e obter o token.

### Validação de ingredientes

O endpoint `POST /validation/` recebe dados multipart/form-data:
- `components`: campos de texto repetidos, um por ingrediente (opcional se houver imagem);
- `image`: arquivo de imagem opcional.

A requisição pode conter somente texto, somente imagem ou ambos. O resultado é retornado no campo `allergies`. Uma imagem que não possa ser processada ou da qual não seja possível extrair texto retorna erro HTTP 422.

A documentação em `/docs` é a referência mais atual para os schemas, parâmetros e respostas.

## Testes automatizados

Com o ambiente Python e as dependências instaladas:

```bash
pytest -q
```

A última execução local registrada foi de **51 testes aprovados e 2 warnings**. A suíte também é executada automaticamente pelo GitHub Actions a cada push para `main` e em pull requests. Confirme o status do workflow após enviar mudanças.

A suíte inclui testes de usuários e autenticação, gerenciamento e isolamento de alergias e regras de validação. Os testes automatizados não substituem a verificação manual do fluxo completo pela interface.

## Estrutura do projeto

A estrutura abaixo resume os diretórios e arquivos principais:

```text
api-read-ingredients/
├── app/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── database.py
│   └── main.py
├── static/
├── templates/
├── tests/
├── migrations/
│   ├── env.py
│   └── versions/
├── alembic.ini
├── init_db.py
├── scripts/
│   └── prepare_database.py
├── Dockerfile
├── start.sh
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Estado atual e próximos passos

O backend já contempla cadastro e autenticação, controle de acesso por usuário, gerenciamento individual de alergias e validação por texto/imagem. O frontend de login e validação também foi integrado.

Estado do projeto: fluxos principais foram implementados e testados manualmente; o esquema atual do PostgreSQL foi conferido; migrações Alembic, proteção do contexto Docker e workflow de testes automatizados estão versionados. Próxima etapa: validar o workflow no GitHub, registrar a revisão no banco local existente e concluir a configuração do ambiente de deploy. O Compose deste repositório é para desenvolvimento local, não uma configuração de produção pronta para exposição pública.

## Deploy no Render

O arquivo `render.yaml` prepara um serviço web baseado no Dockerfile. Ao configurar o Blueprint, informe em `DATABASE_URL` a URL de um PostgreSQL externo persistente; a Blueprint não cria um banco de dados nem armazena credenciais no repositório. A chave `JWT_SECRET_KEY` é gerada pelo Render.

O Dockerfile usa `/app/start.sh` como comando de inicialização: ele chama `scripts/prepare_database.py` e só depois inicia a API. No Render, deixe o campo **Docker Command** vazio para usar o comando padrão da imagem. O preparador aplica a migração inicial em banco vazio; atualiza bancos já gerenciados pelo Alembic; e, em banco legado, registra a revisão inicial somente quando as tabelas `users` e `allergies`, colunas, índices e chave estrangeira correspondem ao esquema antigo conhecido. Se encontrar uma estrutura inesperada, interrompe a inicialização sem tentar recriar tabelas. Faça backup do banco antes de trocar a implantação e confirme a variável `DATABASE_URL` para apontar ao PostgreSQL que deve ser preservado.

A aplicação disponibiliza `GET /health` para validar a conexão ao banco. O serviço gratuito do Render pode entrar em suspensão após inatividade; escolha o plano conforme a necessidade da demonstração. Confira também as condições de persistência e retenção do provedor de PostgreSQL escolhido antes de guardar dados reais.

## Licença

O repositório contém um arquivo [LICENSE](LICENSE). Consulte-o para os termos de utilização e distribuição.

## Autor

**Thiago Henrique**

- GitHub: [Thiago3011](https://github.com/Thiago3011)
- Repositório: [Allergy Validator](https://github.com/Thiago3011/api-read-ingredients)
