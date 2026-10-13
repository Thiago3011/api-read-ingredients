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

Crie um arquivo `.env` na raiz. Use valores locais de desenvolvimento e não publique secrets reais:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/allergy_validator
JWT_SECRET_KEY=replace-with-a-long-random-secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
TESSERACT_CMD=
```

No Docker Compose, a API acessa o banco pelo hostname interno `postgres`. O `docker-compose.yml` define `DATABASE_URL` e também `TESSERACT_CMD=/usr/bin/tesseract`, que é o caminho do executável dentro do container Linux. Isso evita que um caminho de Tesseract específico do Windows, configurado no `.env` local, seja usado dentro do container. Para executar o Python diretamente no Windows, configure `TESSERACT_CMD` com o caminho do executável instalado nessa máquina. Mantenha `JWT_SECRET_KEY` definido no `.env` local para o ambiente de desenvolvimento e nunca publique uma chave real.

Construa e inicie os serviços:

```bash
docker compose up -d --build
```

Confira os containers:

```bash
docker compose ps
docker compose logs -f api
```

Acesse a aplicação web em [http://localhost:8000](http://localhost:8000) e a documentação interativa em [http://localhost:8000/docs](http://localhost:8000/docs).

Para parar os containers:

```bash
docker compose down
```

O banco usa o volume Docker `postgres_data`, destinado a preservar os dados quando os containers são recriados. Evite usar `docker compose down -v` se quiser manter esse volume.

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

A última execução registrada durante o desenvolvimento foi de **48 testes aprovados e 3 warnings**. Esse número deve ser confirmado novamente após alterações futuras.

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
├── init_db.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Estado atual e próximos passos

O backend já contempla cadastro e autenticação, controle de acesso por usuário, gerenciamento individual de alergias e validação por texto/imagem. O frontend de login e validação também foi integrado.

Próximas etapas do projeto:
- concluir testes manuais do fluxo completo;
- revisar persistência do banco e reinicialização dos containers;
- revisar variáveis e configuração de Docker;
- concluir documentação detalhada da API;
- fazer revisão final de qualidade e segurança;
- preparar deploy e demonstração no portfólio.

## Licença

O repositório contém um arquivo [LICENSE](LICENSE). Consulte-o para os termos de utilização e distribuição.

## Autor

**Thiago Henrique**

- GitHub: [Thiago3011](https://github.com/Thiago3011)
- Repositório: [Allergy Validator](https://github.com/Thiago3011/api-read-ingredients)
