# API Reference — Allergy Validator

Este documento descreve os endpoints expostos pelo backend atual do Allergy Validator. Para conferir schemas e respostas diretamente na aplicação em execução, consulte o Swagger em `/docs`.

**Base URL local:** `http://localhost:8000`

**OpenAPI/Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs)

## Autenticação

Cadastro e login não exigem token. Os demais endpoints listados como protegidos exigem JWT.

Inclua o token no cabeçalho HTTP:

```http
Authorization: Bearer <access_token>
```

O token é obtido por `POST /auth/login`. A validade padrão configurada no projeto é de 30 minutos, por meio de `JWT_EXPIRE_MINUTES`.

Respostas de autenticação comuns:
- `401 Unauthorized`: token inválido ou expirado, ou credenciais de login incorretas.
- `403 Forbidden`: acesso negado por regra de autorização ou ausência de credenciais Bearer, conforme o comportamento do FastAPI/HTTPBearer.

## 1. Criar usuário

`POST /user/`

Não exige autenticação.

### Requisição

```http
POST /user/
Content-Type: application/json
```

```json
{
  "name": "Maria Silva",
  "email": "maria@example.com",
  "password": "uma-senha-segura"
}
```

Campos:
- `name`: nome do usuário.
- `email`: e-mail usado para login.
- `password`: senha enviada para cadastro; a aplicação armazena o hash, não a senha em texto puro.

### Resposta de sucesso — 200

```json
{
  "id": 1,
  "name": "Maria Silva",
  "email": "maria@example.com"
}
```

A senha e o hash não fazem parte do schema de resposta.

### Erros relevantes

- `409 Conflict`: e-mail já cadastrado.
- `422 Unprocessable Entity`: corpo ausente ou incompatível com o schema.

## 2. Login

`POST /auth/login`

Não exige autenticação.

### Requisição

```http
POST /auth/login
Content-Type: application/json
```

```json
{
  "email": "maria@example.com",
  "password": "uma-senha-segura"
}
```

### Resposta de sucesso — 200

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

Use o valor de `access_token` nas chamadas protegidas.

### Erros relevantes

- `401 Unauthorized`: e-mail inexistente ou senha incorreta. A API usa uma mensagem genérica para ambos os casos.
- `422 Unprocessable Entity`: corpo inválido.

## 3. Consultar o próprio perfil

`GET /user/me`

Exige JWT. Retorna os dados básicos do usuário associado ao token, sem expor senhas ou hashes.

### Exemplo

```http
GET /user/me
Authorization: Bearer <access_token>
```

### Resposta — 200

```json
{
  "id": 1,
  "name": "Maria Silva",
  "email": "maria@example.com"
}
```

A antiga listagem de usuários por `GET /user/` foi removida para não disponibilizar os dados de todos os usuários a qualquer conta autenticada.

## 4. Consultar usuário por ID

`GET /user/{user_id}`

Exige JWT. O usuário autenticado só pode consultar o próprio ID. Para obter o próprio perfil sem informar um ID, use `GET /user/me`.

### Exemplo

```http
GET /user/1
Authorization: Bearer <access_token>
```

### Resposta — 200

```json
{
  "id": 1,
  "name": "Maria Silva",
  "email": "maria@example.com"
}
```

### Erros relevantes

- `403 Forbidden`: tentativa de consultar outro usuário.
- `401 Unauthorized`: token inválido ou expirado.

## 5. Atualizar usuário

`PATCH /user/{user_id}`

Exige JWT e o usuário autenticado só pode atualizar o próprio ID.

### Requisição

Envie apenas os campos que deseja alterar:

```http
PATCH /user/1
Authorization: Bearer <access_token>
Content-Type: application/json
```

```json
{
  "name": "Maria S. Silva"
}
```

Os campos disponíveis são `name`, `email` e `password`; cada um pode ser omitido.

### Resposta de sucesso — 200

Retorna o usuário com `id`, `name` e `email`. A senha não é retornada.

### Erros relevantes

- `403 Forbidden`: tentativa de atualizar outro usuário.
- `404 Not Found`: usuário não encontrado.
- `409 Conflict`: o e-mail informado já está registrado.
- `422 Unprocessable Entity`: corpo inválido.

## 6. Excluir usuário

`DELETE /user/{user_id}`

Exige JWT e o usuário autenticado só pode excluir o próprio ID.

Exemplo:

```http
DELETE /user/1
Authorization: Bearer <access_token>
```

### Resposta de sucesso — 204

Sem corpo de resposta.

### Erros relevantes

- `403 Forbidden`: tentativa de excluir outro usuário.
- `404 Not Found`: usuário não encontrado.
- `401 Unauthorized`: token inválido ou expirado.

## 7. Listar as próprias alergias

`GET /user/allergies/`

Exige JWT. A lista retornada pertence ao usuário autenticado.

Exemplo:

```http
GET /user/allergies/
Authorization: Bearer <access_token>
```

### Resposta — 200

```json
[
  {
    "id": 1,
    "name": "Amendoim",
    "user_id": 1
  },
  {
    "id": 2,
    "name": "Leite",
    "user_id": 1
  }
]
```

A resposta é uma lista; se o usuário ainda não cadastrou alergias, a lista fica vazia.

## 8. Cadastrar alergia

`POST /user/allergies/?name={nome}`

Exige JWT. O nome é recebido como **parâmetro de query string**, não como JSON.

### Exemplo

```http
POST /user/allergies/?name=Amendoim
Authorization: Bearer <access_token>
```

Com cURL:

```bash
curl -X POST "http://localhost:8000/user/allergies/?name=Amendoim" \
  -H "Authorization: Bearer <access_token>"
```

### Resposta de sucesso — 200

```json
{
  "id": 1,
  "name": "Amendoim",
  "user_id": 1
}
```

O nome é removido de espaços no início e no fim. Se ficar vazio, a API retorna `422`.

## 9. Excluir alergia

`DELETE /user/allergies/{allergy_id}`

Exige JWT. Só é possível excluir uma alergia pertencente ao usuário autenticado.

Exemplo:

```http
DELETE /user/allergies/1
Authorization: Bearer <access_token>
```

### Resposta de sucesso — 200

```json
{
  "message": "Alergia removida com sucesso!"
}
```

### Erros relevantes

- `404 Not Found`: alergia não encontrada ou não pertence ao usuário autenticado.
- `401 Unauthorized`: token inválido ou expirado.

## 10. Validar ingredientes

`POST /validation/`

Exige JWT. O endpoint recebe `multipart/form-data` e aceita texto, imagem ou ambos na mesma requisição.

### Campos

| Campo | Tipo | Obrigatório |
|---|---|---|
| `components` | Texto; pode ser enviado repetidamente, um ingrediente por campo | Não, se uma imagem for enviada |
| `image` | Arquivo de imagem | Não, se ao menos um campo de texto for enviado |

### Exemplo — somente texto

```bash
curl -X POST "http://localhost:8000/validation/" \
  -H "Authorization: Bearer <access_token>" \
  -F "components=Amendoim" \
  -F "components=Farinha de trigo"
```

### Exemplo — somente imagem

```bash
curl -X POST "http://localhost:8000/validation/" \
  -H "Authorization: Bearer <access_token>" \
  -F "image=@./rotulo.jpg"
```

### Exemplo — texto e imagem

```bash
curl -X POST "http://localhost:8000/validation/" \
  -H "Authorization: Bearer <access_token>" \
  -F "components=Amendoim" \
  -F "image=@./rotulo.jpg"
```

### Resposta de sucesso — 200

```json
{
  "allergies": [
    "Amendoim"
  ]
}
```

O campo `allergies` contém os componentes que corresponderam às alergias cadastradas pelo usuário. Se nenhuma correspondência for encontrada, o campo será uma lista vazia.

### Erros relevantes

- `401 Unauthorized`: token inválido ou expirado.
- `422 Unprocessable Entity`: a imagem não pôde ser processada ou não foi possível extrair texto.
- `422 Unprocessable Entity`: campos de formulário em formato inválido.

### Limitações atuais da comparação

- A comparação de componentes informados manualmente é textual e não diferencia maiúsculas de minúsculas.
- Na análise de OCR, o serviço procura os nomes das alergias no texto extraído.
- Sinônimos, nomes alternativos, erros de leitura do OCR e ingredientes não reconhecidos pelo texto podem não ser detectados.

Por isso, o resultado deve ser tratado como apoio e não como garantia de ausência ou presença de alérgenos.

## Códigos HTTP comuns

| Código | Significado no contexto da API |
|---|---|
| `200 OK` | Requisição processada com sucesso |
| `204 No Content` | Exclusão de usuário concluída, sem corpo de resposta |
| `401 Unauthorized` | Token inválido/expirado ou credenciais incorretas no login |
| `403 Forbidden` | Regra de autorização não permite a operação ou falta de credenciais Bearer |
| `404 Not Found` | Usuário ou alergia não encontrada |
| `409 Conflict` | E-mail já cadastrado |
| `422 Unprocessable Entity` | Entrada inválida ou falha ao processar a imagem |

A validação detalhada de parâmetros, schemas e respostas continua disponível no Swagger da aplicação em execução: `http://localhost:8000/docs`.
