# API de Estoque

![CI](https://github.com/Tobias-Lopes/estoque-api/actions/workflows/ci.yml/badge.svg)

Sistema de gerenciamento de estoque desenvolvido com **Python, FastAPI, SQLAlchemy e Vue 3**, permitindo controlar produtos, registrar movimentações, calcular custos e preços de venda e importar dados por CSV.

O projeto foi desenvolvido com foco em boas práticas de desenvolvimento back-end, organização de código, testes automatizados e integração contínua.

## Funcionalidades

- Cadastro de produtos com SKU único.
- Listagem e consulta de produtos.
- Filtro de produtos com estoque baixo.
- Registro de compras e entradas de estoque.
- Cálculo automático do custo médio ponderado.
- Registro de vendas e saídas de estoque.
- Validação de estoque disponível.
- Atualização da margem de acréscimo.
- Cálculo automático do preço de venda.
- Histórico de movimentações.
- Importação de produtos por CSV utilizando pandas.
- Interface web desenvolvida em Vue 3.

## Tecnologias

| Camada | Tecnologias |
|---|---|
| Backend | Python 3.12, FastAPI, Pydantic |
| ORM | SQLAlchemy 2.0 |
| Banco de dados | PostgreSQL e SQLite |
| Frontend | Vue 3, JavaScript, Vite |
| Processamento de dados | pandas |
| Testes | pytest, Vitest, HTTPX |
| Infraestrutura | Docker, Docker Compose |
| CI | GitHub Actions |

## Arquitetura

O sistema utiliza uma arquitetura cliente-servidor, com frontend e backend separados.

```text
Frontend (Vue 3)
       |
       | HTTP / JSON
       v
Backend (FastAPI)
       |
       | Pydantic
       | Validação de dados
       |
       | SQLAlchemy
       | Regras de negócio
       v
Banco de dados
(PostgreSQL / SQLite)
```

O frontend é responsável pela interface e interação com o usuário.

O backend processa as requisições HTTP, valida os dados e executa as regras de negócio.

O SQLAlchemy realiza o mapeamento entre os objetos Python e as tabelas do banco de dados.

## Estrutura do projeto

```text
estoque-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── pricing.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.vue
│   │   ├── api.js
│   │   ├── format.js
│   │   └── style.css
│   └── package.json
├── scripts/
│   └── importar_csv.py
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_pricing.py
│   ├── test_schemas.py
│   └── test_importar_csv.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

### Organização do backend

- `main.py`: endpoints HTTP e integração das regras de negócio.
- `database.py`: configuração do SQLAlchemy e sessões.
- `models.py`: modelos ORM de produtos e movimentações.
- `schemas.py`: schemas Pydantic e validações.
- `pricing.py`: funções de cálculo de preço e custo médio.

## Como executar

### Pré-requisitos

- Python 3.12
- Node.js compatível com a versão do Vite instalada
- npm
- Git
- Docker Desktop (para execução com PostgreSQL)

### 1. Clonar o repositório

```bash
git clone https://github.com/Tobias-Lopes/estoque-api.git
cd estoque-api
```

### 2. Executar o backend localmente

No Windows, utilizando PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m uvicorn app.main:app --reload
```

A API estará disponível em:

`http://localhost:8000`

Documentação Swagger:

`http://localhost:8000/docs`

Nesta configuração, a aplicação utiliza SQLite como banco de dados local.

### 3. Executar com Docker e PostgreSQL

Com o Docker Desktop funcionando, execute na raiz:

```bash
docker compose up --build -d
```

O Docker Compose inicializa os serviços da API e do PostgreSQL.

Para acompanhar os containers:

```bash
docker compose ps
```

Para visualizar os logs:

```bash
docker compose logs -f api
```

Para encerrar os serviços:

```bash
docker compose down
```

O PostgreSQL utiliza um volume nomeado para preservar os dados entre reinicializações dos containers.

### 4. Executar o frontend

Com o backend disponível na porta 8000, abra outro terminal:

```bash
cd frontend
npm install
npm run dev
```

A aplicação Vue estará disponível em:

`http://localhost:5173`

Durante o desenvolvimento, o Vite utiliza um proxy para encaminhar as requisições `/api` ao FastAPI.

## Endpoints da API

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/health` | Verificar disponibilidade |
| POST | `/produtos` | Cadastrar produto |
| GET | `/produtos` | Listar produtos |
| GET | `/produtos/{id}` | Consultar produto |
| PATCH | `/produtos/{id}/margem` | Atualizar margem |
| POST | `/produtos/{id}/compras` | Registrar compra |
| POST | `/produtos/{id}/saidas` | Registrar saída |
| GET | `/produtos/{id}/movimentacoes` | Consultar histórico |

O endpoint `GET /produtos` aceita o parâmetro opcional `estoque_max` para filtrar produtos com estoque abaixo ou igual ao valor informado.

### Exemplo de cadastro

**POST /produtos**

```json
{
  "sku": "CAF-001",
  "nome": "Café 500g",
  "margem_percentual": 50
}
```

### Exemplo de compra

**POST /produtos/1/compras**

```json
{
  "quantidade": 10,
  "custo_unitario_centavos": 1000
}
```

### Exemplo de saída

**POST /produtos/1/saidas**

```json
{
  "quantidade": 4
}
```

Os valores monetários são representados por inteiros em centavos.

Por exemplo, `1000` equivale a R$ 10,00.

## Regras de negócio

### Custo médio ponderado

O custo médio é atualizado sempre que uma compra é registrada.

A fórmula utilizada é:

\[
C_{\text{novo}} =
\frac{Q_{\text{atual}}\cdot C_{\text{atual}}+Q_{\text{compra}}\cdot C_{\text{compra}}}
{Q_{\text{atual}}+Q_{\text{compra}}}
\]

Exemplo:

- Estoque atual: 10 unidades a R$ 10,00.
- Nova compra: 10 unidades a R$ 20,00.
- Novo estoque: 20 unidades.
- Novo custo médio: R$ 15,00.

Os cálculos são realizados em centavos, com arredondamento para valores inteiros.

### Preço de venda

O preço é calculado a partir do custo médio e da margem de acréscimo:

\[
P = C \times \left(1+\frac{M}{100}\right)
\]

Para um produto com custo médio de R$ 15,00 e margem de 50%, o preço será R$ 22,50.

O preço de venda é uma propriedade calculada, não uma coluna persistida no banco.

### Controle de estoque

Uma saída somente é permitida quando existe estoque suficiente.

Quando a quantidade solicitada supera a disponível, a API retorna HTTP 409 Conflict.

As operações de atualização do estoque e registro de movimentação são realizadas na mesma transação do banco de dados.

## Importação de CSV

O projeto possui um script para cadastrar produtos a partir de arquivos CSV utilizando pandas.

Formato esperado:

```csv
sku,nome,margem_percentual
TEC-001,Teclado,40
MOU-001,Mouse,30
MON-001,Monitor,35
```

Com a API em execução, utilize:

```bash
python -m scripts.importar_csv produtos.csv http://localhost:8000
```

O script valida os dados antes de iniciar o envio.

Se houver erros de validação no CSV, a importação é cancelada antes de qualquer requisição. Os cadastros enviados após a validação, entretanto, são requisições independentes e não formam uma única transação.

## Testes automatizados

### Backend

O backend utiliza pytest para testes de funções, validações e endpoints HTTP.

Os testes de integração utilizam SQLite em memória e sobrescrita de dependências do FastAPI para isolar o banco de cada execução.

Na raiz do projeto:

```bash
python -m pytest -v
```

### Frontend

O frontend utiliza Vitest para testar conversões monetárias, tratamento de erros e chamadas HTTP simuladas.

```bash
cd frontend
npm test
```

Para validar o build:

```bash
npm run build
```

## Integração contínua

O projeto utiliza GitHub Actions para executar verificações automáticas a cada push e pull request.

O workflow está em `.github/workflows/ci.yml`.

Ele contém três jobs principais:

1. **Backend:** instala dependências e executa os testes Python.
2. **Frontend:** executa os testes Vitest e compila o projeto Vue.
3. **Docker:** valida a configuração e constrói a imagem da aplicação após os testes.

O pipeline realiza integração contínua. Não há deploy automático configurado.

## Decisões técnicas

- **SQLAlchemy:** abstração do acesso ao banco utilizando ORM.
- **Pydantic:** validação declarativa dos dados de entrada e saída.
- **Valores em centavos:** redução de imprecisões com ponto flutuante.
- **Funções de precificação isoladas:** facilidade de manutenção e testes unitários.
- **Transações:** consistência entre estoque e movimentações.
- **SELECT FOR UPDATE:** bloqueio de linhas em bancos compatíveis, como PostgreSQL, para operações concorrentes de estoque.
- **Testes com banco isolado:** independência entre cenários e proteção dos dados locais.
- **Docker Compose:** execução integrada da API e do PostgreSQL.
- **GitHub Actions:** execução automatizada das verificações de qualidade.

## Limitações e possíveis melhorias

- Implementar autenticação e autorização de usuários.
- Utilizar Alembic para migrações do banco de dados.
- Implementar paginação na listagem de produtos.
- Criar uma tela de histórico de movimentações no frontend.
- Adicionar testes automatizados de componentes Vue.
- Implementar importação CSV com transação única e política de atualização de produtos existentes.
- Configurar deploy da aplicação em ambiente de produção.

## Objetivo do projeto

Projeto desenvolvido para aprofundamento prático em Python e desenvolvimento full stack, abrangendo APIs REST, persistência de dados, validação, regras de negócio, testes automatizados, processamento de CSV, containers e integração contínua.
