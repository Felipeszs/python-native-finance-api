# Frontend Transactions

## 1. Context

A Finance API atualmente possui endpoints HTTP para gerenciamento de transações.

O objetivo desta feature é criar uma interface web simples para permitir que a API seja utilizada e testada diretamente através do navegador.

O frontend será inicialmente utilizado como cliente da API e não como uma aplicação completa.

---

## 2. Goal

Permitir que o usuário:

- visualize todas as transações cadastradas;
- crie novas transações;
- visualize erros retornados pela API.

---

## 3. Scope

Esta versão deve implementar:

- listagem de transações;
- criação de transações;
- estado vazio;
- estado de carregamento;
- tratamento básico de erros.

---

## 4. Out of Scope

Não implementar nesta versão:

- edição;
- exclusão;
- autenticação;
- paginação;
- filtros;
- gráficos;
- dashboard financeiro;
- categorias;
- persistência local;
- framework frontend.

Esses recursos serão adicionados somente quando existirem requisitos correspondentes no backend.

---

# 5. Functional Requirements

## FR-01 — Listar transações

Ao carregar a página, o frontend deve solicitar todas as transações através de:

GET /transactions

As transações retornadas devem ser exibidas na interface.

---

## FR-02 — Estado vazio

Caso a API retorne uma lista vazia, o frontend deve mostrar uma mensagem informando que ainda não existem transações cadastradas.

Exemplo:

"Nenhuma transação cadastrada."

---

## FR-03 — Criar transação

O usuário deve conseguir cadastrar uma nova transação através de um formulário.

O formulário deve possuir:

- transaction_type;
- value;
- description.

---

## FR-04 — Tipos de transação

O campo transaction_type deve permitir:

- income;
- expense.

---

## FR-05 — Enviar transação

Ao enviar o formulário, o frontend deve realizar:

POST /transactions

Content-Type:

application/json

Payload esperado:

```json
{
  "transaction_type": "income",
  "value": "100.00",
  "description": "Example"
}
```

---

## FR-06 — Atualização após criação

Caso a criação seja realizada com sucesso, a nova transação deve aparecer na listagem.

O frontend pode atualizar a lista executando novamente:

GET /transactions

---

## FR-07 — Tratamento de erro

Caso a API retorne erro, o frontend deve informar o usuário.

A interface não deve simplesmente falhar silenciosamente.

---

## FR-08 — Loading

Enquanto as transações estiverem sendo carregadas, a interface deve mostrar algum estado visual de carregamento.

---

# 6. API Contract

## List Transactions

Request:

GET /transactions

Expected response:

```json
[
  {
    "id": 1,
    "type": "income",
    "value": "500.00",
    "description": "Salary"
  }
]
```

---

## Create Transaction

Request:

POST /transactions

Headers:

Content-Type: application/json

Body:

```json
{
  "transaction_type": "expense",
  "value": "50.00",
  "description": "Market"
}
```

Successful response:

HTTP 201

```json
{
  "id": 2,
  "type": "expense",
  "value": "50.00",
  "description": "Market"
}
```

---

# 7. User Interface

A página deve possuir duas áreas principais.

## Transaction Form

Campos:

- Type
- Value
- Description

Ação:

- Add Transaction

---

## Transaction List

Cada transação deve mostrar:

- id;
- descrição;
- tipo;
- valor.

Exemplo:

```text
Transactions

Salary
Income
R$ 500.00

Market
Expense
R$ 50.00
```

---

# 8. Technical Design

Tecnologias:

- HTML5;
- CSS;
- JavaScript;
- Fetch API.

Não utilizar framework frontend nesta versão.

---

## Application Flow

```text
Browser
   ↓
index.html
   ↓
app.js
   ↓
fetch()
   ↓
HTTP
   ↓
Finance API
```

Backend:

```text
Server
↓
Router
↓
Controller
↓
Service
↓
Repository
↓
Model
```

Response:

```text
Model
↓
View
↓
JSON
↓
HTTP Response
↓
JavaScript
↓
DOM
```

---

# 9. JavaScript Responsibilities

O frontend deve possuir responsabilidades equivalentes a:

```text
loadTransactions()

createTransaction()

renderTransactions()

showError()

setLoading()
```

### loadTransactions

Responsável por executar:

GET /transactions

e enviar os dados para renderização.

### createTransaction

Responsável por:

- coletar os dados do formulário;
- criar o payload;
- executar POST /transactions.

### renderTransactions

Responsável apenas por transformar os dados recebidos em elementos visuais.

### showError

Responsável por mostrar erros ao usuário.

---

# 10. Acceptance Criteria

## AC-01

Given que existem transações

When o usuário abrir a página

Then GET /transactions deve ser executado

And as transações devem aparecer na interface.

---

## AC-02

Given que nenhuma transação existe

When GET /transactions retornar []

Then deve ser exibida uma mensagem de estado vazio.

---

## AC-03

Given que o formulário está preenchido corretamente

When o usuário clicar em Add Transaction

Then POST /transactions deve ser executado.

---

## AC-04

Given que POST /transactions retornou HTTP 201

When a transação for criada

Then a listagem deve ser atualizada.

---

## AC-05

Given que a API retorna erro

When uma operação falhar

Then uma mensagem deve ser exibida ao usuário.

---

# 11. Tasks

## Setup

- [ ] Criar pasta `frontend`
- [ ] Criar `index.html`
- [ ] Criar `styles.css`
- [ ] Criar `app.js`

## Interface

- [ ] Criar cabeçalho
- [ ] Criar formulário
- [ ] Criar seletor income/expense
- [ ] Criar campo value
- [ ] Criar campo description
- [ ] Criar botão Add Transaction
- [ ] Criar container da lista

## GET

- [ ] Criar `loadTransactions`
- [ ] Executar GET /transactions
- [ ] Converter Response para JSON
- [ ] Criar `renderTransactions`
- [ ] Implementar estado vazio
- [ ] Implementar loading

## POST

- [ ] Capturar submit do formulário
- [ ] Criar payload
- [ ] Executar POST /transactions
- [ ] Enviar Content-Type application/json
- [ ] Tratar HTTP 201
- [ ] Limpar formulário
- [ ] Recarregar lista

## Error Handling

- [ ] Tratar erro de conexão
- [ ] Tratar erros HTTP
- [ ] Mostrar mensagem na interface

---

# 12. Definition of Done

A feature estará concluída quando:

- a página abrir corretamente;
- GET /transactions funcionar;
- as transações forem exibidas;
- estado vazio funcionar;
- o formulário criar uma transação;
- POST /transactions funcionar;
- a lista atualizar depois da criação;
- erros forem mostrados ao usuário;
- nenhuma funcionalidade fora do escopo tiver sido adicionada.
