# Python Native Finance API

API REST de gerenciamento financeiro desenvolvida com Python e sua biblioteca padrão, sem utilização de frameworks web.

O projeto foi criado com objetivo educacional para estudar os fundamentos de desenvolvimento backend e Engenharia de Software, implementando manualmente conceitos que normalmente são abstraídos por frameworks como Django, Flask e FastAPI.

## Objetivos

O principal objetivo deste projeto é compreender, na prática:

* funcionamento de uma API HTTP;
* arquitetura MVC;
* orientação a objetos;
* separação de responsabilidades;
* baixo acoplamento e alta coesão;
* princípios SOLID;
* camada de serviços;
* Repository Pattern;
* Dependency Injection;
* persistência de dados;
* tratamento de erros;
* testes automatizados;
* design de APIs REST.

A arquitetura e os padrões serão introduzidos progressivamente conforme surgirem necessidades reais no projeto, evitando complexidade desnecessária.

## Tecnologias

* Python
* Python Standard Library
* `http.server`
* `json`
* `unittest`

Inicialmente, o projeto não utiliza frameworks ou bibliotecas externas.

## Arquitetura

O projeto utiliza MVC com algumas camadas adicionais para melhorar a separação de responsabilidades.

```text
Request
   ↓
Router
   ↓
Controller
   ↓
Service
   ↓
Model
   ↓
Repository
```

A resposta percorre o caminho inverso e é representada pela camada de View.

```text
Model
  ↓
View
  ↓
JSON
  ↓
HTTP Response
```

### Estrutura

```text
python-native-finance-api/
│
├── app/
│   ├── controllers/
│   ├── models/
│   ├── repositories/
│   ├── routes/
│   ├── services/
│   └── views/
│
├── tests/
│
├── main.py
└── README.md
```

## Funcionalidades planejadas

### V1 — Fundamentos

* [ ] Entidade Transaction
* [ ] Armazenamento em memória
* [ ] POST `/transactions`
* [ ] GET `/transactions`
* [ ] Servidor HTTP utilizando Python nativo
* [ ] Arquitetura MVC

### V2 — CRUD

* [ ] GET `/transactions/{id}`
* [ ] PUT `/transactions/{id}`
* [ ] DELETE `/transactions/{id}`

### V3 — Persistência

* [ ] SQLite
* [ ] Repository para persistência
* [ ] Migração do armazenamento em memória para banco de dados

### V4 — Robustez

* [ ] Validações
* [ ] Exceções customizadas
* [ ] Tratamento centralizado de erros
* [ ] Status HTTP adequados

### V5 — Arquitetura

* [ ] Interfaces de repositories
* [ ] Dependency Inversion
* [ ] Dependency Injection
* [ ] Refatoração das responsabilidades

### V6 — Testes

* [ ] Testes unitários
* [ ] Testes de integração
* [ ] Testes dos endpoints

### Futuro

* [ ] Usuários
* [ ] Autenticação
* [ ] Paginação
* [ ] Filtros
* [ ] Relatórios financeiros

## Domínio inicial

A primeira entidade do sistema será `Transaction`.

Uma transação possuirá:

* `id`
* `description`
* `value`
* `type`

Os tipos permitidos serão:

* `income`
* `expense`

## Status

🚧 Projeto em desenvolvimento.

A arquitetura será evoluída gradualmente durante o desenvolvimento para estudar os problemas e decisões que levam à adoção de diferentes padrões de Engenharia de Software.
