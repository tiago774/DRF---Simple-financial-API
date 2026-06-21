# API Financeira - Django REST Framework

API RESTful para gerenciamento de instituição financeira, desenvolvida com Django REST Framework.

## Funcionalidades

- Cadastro de clientes (pessoa física e jurídica)
- Gerenciamento de contas bancárias
- Registro de transações (depósitos, saques, pagamentos)
- Autenticação e permissões por usuário
- Validação de CPF/CNPJ
- Versionamento de API
- Testes automatizados

## Requisitos

- Python 3.8+
- Django 5.0.3+
- Django REST Framework

## Instalação

### 1. Clone o repositório


git clone https://github.com/tiago774/DRF---Simple-financial-API.git
cd DRF


### 2. Crie e ative o ambiente virtual


python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows


### 3. Instale as dependências


pip install -r requirements.txt


### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3


### 5. Execute as migrações


python manage.py migrate


### 6. Crie um superusuário


python manage.py createsuperuser


### 7. Execute o servidor


python manage.py runserver


A API estará disponível em: `http://localhost:8000/`

## Endpoints da API

### Clientes

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| GET | `/clientes/` | Lista todos os clientes |
| POST | `/clientes/` | Cria um novo cliente |
| GET | `/clientes/{id}/` | Detalhes de um cliente |
| PUT | `/clientes/{id}/` | Atualiza um cliente |
| DELETE | `/clientes/{id}/` | Remove um cliente |
| GET | `/clientes/{id}/contas/` | Lista contas de um cliente |

### Contas

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| GET | `/contas/` | Lista todas as contas |
| POST | `/contas/` | Cria uma nova conta |
| GET | `/contas/{id}/` | Detalhes de uma conta |
| PUT | `/contas/{id}/` | Atualiza uma conta |
| GET | `/contas/{id}/extrato/` | Extrato da conta |

### Transacoes

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| GET | `/transacoes/` | Lista todas as transacoes |
| POST | `/transacoes/` | Cria uma nova transacao |
| GET | `/transacoes/{id}/` | Detalhes de uma transacao |

## Exemplos de Uso

### Autenticacao

Todas as requisicoes exigem autenticacao Basic Auth:


# Usuario: admin
# Senha: admin123


### Criar um Cliente


curl -X POST http://localhost:8000/clientes/ \
  -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Joao Silva",
    "email": "joao@email.com",
    "cpf_cnpj": "529.982.247-25",
    "tipo_pessoa": "F",
    "telefone": "(11) 99999-9999"
  }'


### Criar uma Conta


curl -X POST http://localhost:8000/contas/ \
  -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": 1,
    "numero": "12345-6",
    "agencia": "0001",
    "tipo_conta": "CC"
  }'


### Realizar um Deposito


curl -X POST http://localhost:8000/transacoes/ \
  -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "conta": 1,
    "tipo": "D",
    "valor": 500.00,
    "descricao": "Deposito inicial"
  }'


### Consultar Extrato


curl -X GET http://localhost:8000/contas/1/extrato/ \
  -u admin:admin123


### Listar Clientes

curl -X GET http://localhost:8000/clientes/ \
  -u admin:admin123

### Buscar Clientes por Nome

curl -X GET "http://localhost:8000/clientes/?search=Joao" \
  -u admin:admin123

### Filtrar Contas por Tipo

curl -X GET "http://localhost:8000/contas/?tipo_conta=CC" \
  -u admin:admin123

## Versionamento da API

A API suporta versionamento via query parameter:


# Versao 1 (padrao)
curl -X GET http://localhost:8000/clientes/ \
  -u admin:admin123

# Versao 2
curl -X GET "http://localhost:8000/clientes/?version=v2" \
  -u admin:admin123


## Modelos de Dados

### Cliente

| Campo | Tipo | Descricao |
|-------|------|-----------|
| id | Integer | Identificador unico |
| nome | String | Nome completo |
| email | String | E-mail |
| cpf_cnpj | String | CPF ou CNPJ (unico) |
| tipo_pessoa | String | F (Fisica) ou J (Juridica) |
| telefone | String | Telefone no formato (XX) XXXXX-XXXX |
| ativo | Boolean | Cliente ativo ou inativo |

### Conta

| Campo | Tipo | Descricao |
|-------|------|-----------|
| id | Integer | Identificador unico |
| cliente | Integer | ID do cliente |
| numero | String | Numero da conta (unico) |
| agencia | String | Agencia |
| tipo_conta | String | CC (Corrente), CP (Poupanca), CI (Investimento) |
| saldo | Decimal | Saldo atual |
| ativa | Boolean | Conta ativa ou inativa |

### Transacao

| Campo | Tipo | Descricao |
|-------|------|-----------|
| id | Integer | Identificador unico |
| conta | Integer | ID da conta |
| tipo | String | D (Deposito), S (Saque), T (Transferencia), P (Pagamento) |
| valor | Decimal | Valor da transacao |
| descricao | String | Descricao opcional |
| data_transacao | DateTime | Data e hora da transacao |

## Validacoes

- CPF/CNPJ valido (formato com pontos e tracos)
- Nome contem apenas letras e espacos
- Telefone no formato (XX) XXXXX-XXXX
- Valor da transacao deve ser positivo
- Saldo insuficiente para saques e pagamentos

## Testes

Execute os testes automatizados:

python manage.py test financeiro --verbosity=2

## Licenca

Este projeto esta sob a licenca MIT.# DRF---Simple-financial-API
