# Allergy Validator

![Allergy Validator](./static/images/irritacao-na-pele.png)

API para identificação de possíveis componentes alergênicos a partir de ingredientes informados manualmente ou extraídos de imagens utilizando OCR.

O projeto foi desenvolvido inicialmente para resolver um problema real e, posteriormente, revisitado com foco em organização arquitetural, testes, persistência de dados e evolução do backend.

---

## Sobre o projeto

O Allergy Validator permite que o usuário informe ingredientes manualmente ou envie uma imagem contendo uma lista de ingredientes.

Quando uma imagem é enviada, o sistema utiliza OCR para extrair o texto e então verifica se existem componentes correspondentes às alergias cadastradas.

O projeto está sendo reconstruído utilizando uma arquitetura mais organizada, separando responsabilidades entre API, serviços, repositórios e modelos de dados.

---

## Funcionalidades

- Entrada manual de ingredientes
- Upload de imagens
- Extração de texto utilizando OCR
- Processamento e correção do texto extraído
- Cadastro de componentes relacionados a alergias
- Validação dos ingredientes informados
- Validação de componentes encontrados através de OCR
- API REST com FastAPI
- Persistência utilizando PostgreSQL
- Testes automatizados com Pytest
- Execução da aplicação utilizando Docker
- Docker Compose para ambiente local com API + PostgreSQL

---

## Tecnologias

### Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Psycopg

### Processamento de imagens

- Tesseract OCR
- Pytesseract
- Pillow
- Pillow-Heif
- PySpellChecker

### Testes

- Pytest

### Infraestrutura

- Docker
- Docker Compose

### Frontend

- HTML
- CSS
- JavaScript

---

## Arquitetura

O projeto utiliza uma arquitetura organizada por responsabilidades:

```text
app/
├── core/
│   └── config.py
│
├── models/
│   ├── allergy.py
│   └── user.py
│
├── repositories/
│   └── allergy_repository.py
│
├── routers/
│   └── validation.py
│
├── schemas/
│
├── services/
│   ├── allergy_service.py
│   └── image_processor.py
│
├── database.py
└── main.py
```

### Responsabilidades

**Routers**

Responsáveis pelos endpoints da API e pela comunicação entre as requisições HTTP e os serviços da aplicação.

**Services**

Contêm as regras de negócio e o processamento das informações.

**Repositories**

Responsáveis pelo acesso aos dados persistidos no banco.

**Models**

Representam as entidades utilizadas pelo banco de dados através do SQLAlchemy.

**Core**

Contém configurações centrais da aplicação.

---

## Como funciona

O fluxo principal da aplicação pode ser representado da seguinte forma:

```text
Usuário
   │
   ├── Ingredientes
   │
   └── Imagem
          │
          ▼
     FastAPI
          │
          ▼
   ImageProcessor
          │
          ▼
      Texto OCR
          │
          ▼
   AllergyService
          │
          ▼
 AllergyRepository
          │
          ▼
    PostgreSQL
          │
          ▼
    Resultado
```

Quando o usuário envia ingredientes manualmente, eles são encaminhados diretamente para a camada de serviço.

Quando uma imagem é enviada, ela passa primeiro pelo processamento de imagem e OCR. O texto extraído então é utilizado na validação.

---

## Executando com Docker

O projeto possui um `docker-compose.yml` que inicia a API e o PostgreSQL.

### 1. Subir os containers

```bash
docker compose up -d --build
```

### 2. Verificar os containers

```bash
docker compose ps
```

### 3. Acessar a aplicação

Abra:

```text
http://localhost:8000
```

A documentação interativa da API está disponível em:

```text
http://localhost:8000/docs
```

### 4. Parar os containers

```bash
docker compose down
```

---

## Executando localmente

Também é possível executar a aplicação diretamente através de um ambiente virtual Python.

### 1. Criar o ambiente virtual

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar as variáveis de ambiente

Crie um arquivo `.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/allergy_validator
TESSERACT_CMD=C:/Program Files/Tesseract-OCR/tesseract.exe
```

O caminho do Tesseract deve ser ajustado de acordo com o ambiente utilizado.

### 4. Inicializar os dados

Para cadastrar a lista inicial de alergias:

```bash
python -m scripts.seed_allergies
```

### 5. Iniciar a API

```bash
uvicorn app.main:app --reload
```

A aplicação estará disponível em:

```text
http://localhost:8000
```

---

## Testes

Os testes automatizados podem ser executados utilizando:

```bash
pytest -q
```

Atualmente, os testes cobrem principalmente a lógica de identificação de componentes alergênicos, incluindo:

- identificação de alergênico informado manualmente;
- componentes que não são alergênicos;
- identificação através de texto extraído por OCR;
- prevenção de resultados duplicados.

---

## API

A API possui atualmente o endpoint principal:

```http
POST /validation/
```

O endpoint recebe:

- componentes informados pelo usuário;
- opcionalmente, uma imagem para processamento via OCR.

A documentação interativa pode ser acessada através do Swagger:

```text
http://localhost:8000/docs
```

---

## Estrutura do projeto

```text
api-read-ingredients/
│
├── app/
│   ├── core/
│   │   └── config.py
│   │
│   ├── models/
│   │   ├── allergy.py
│   │   ├── user.py
│   │   └── __init__.py
│   │
│   ├── repositories/
│   │   ├── allergy_repository.py
│   │   └── __init__.py
│   │
│   ├── routers/
│   │   ├── validation.py
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── allergy_service.py
│   │   ├── image_processor.py
│   │   └── __init__.py
│   │
│   ├── database.py
│   ├── main.py
│   └── __init__.py
│
├── scripts/
│   ├── seed_allergies.py
│   └── __init__.py
│
├── static/
│   ├── images/
│   │   └── irritacao-na-pele.png
│   ├── index.css
│   └── script.js
│
├── templates/
│   └── index.html
│
├── tests/
│   ├── test_allergy_service.py
│   └── __init__.py
│
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt
```

---

## Próximos passos

O projeto está em processo de evolução e alguns componentes serão adicionados gradualmente.

Entre os próximos passos estão:

- implementação de autenticação e usuários;
- evolução das regras de validação;
- ampliação da cobertura de testes;
- criação de schemas específicos para a API;
- melhorias no tratamento de erros;
- evolução da persistência e dos relacionamentos;
- preparação da aplicação para deploy.

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## Autor

**Thiago Henrique**

[GitHub](https://github.com/Thiago3011)