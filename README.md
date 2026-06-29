# dbt + BigQuery: Pipeline de Dados de Vendas

Pipeline analítico de ponta a ponta que carrega dados transacionais de vendas a partir de arquivos CSV para o Google BigQuery e os transforma em um modelo dimensional (esquema estrela) usando dbt, entregando tabelas analíticas prontas para consumo em ferramentas de BI.

## Visão geral

O projeto cobre o ciclo completo de um data warehouse analítico:

1. **Ingestão:** um script Python carrega cinco arquivos CSV para uma camada bruta (staging) no BigQuery.
2. **Modelagem dimensional:** o dbt transforma os dados brutos em quatro dimensões e uma tabela fato, organizadas em um esquema estrela.
3. **Camada analítica:** três marts agregam o modelo dimensional em visões de negócio (vendas por categoria, por cliente e por mês).

## Arquitetura

```mermaid
flowchart LR
    A[Arquivos CSV] --> B[carrega_dados_bigquery.py]
    B --> C[(BigQuery<br/>dataset dsastaging)]
    C --> D[dbt: camada staging<br/>4 dimensoes + 1 fato]
    D --> E[dbt: camada marts<br/>visoes analiticas]
    E --> F[Consumo em BI]
```

## Stack

| Camada | Tecnologia |
|---|---|
| Ingestão | Python (biblioteca google-cloud-bigquery) |
| Data Warehouse | Google BigQuery |
| Transformação e modelagem | dbt Core 1.8 (adapter BigQuery 1.8) |
| Documentação de modelos | dbt (sources.yml, schema.yml) |

## Modelo de dados

O núcleo do projeto é um **esquema estrela**: uma tabela fato central referenciando quatro dimensões.

### Dimensões

- **dim_clientes:** dados cadastrais dos clientes (id, nome, idade, gênero).
- **dim_data:** dimensão de calendário (ano, mês, dia, trimestre, dia da semana, indicador de fim de semana).
- **dim_localidades:** cidade, estado, país e CEP.
- **dim_produtos:** nome, categoria e preço unitário dos produtos.

### Fato

- **fato_vendas:** transações de venda, ligando as quatro dimensões e registrando quantidade e valor total por transação.

### Marts (visões analíticas)

- **dsa_mart_vendas_por_categoria:** quantidade vendida e valor total agregados por categoria de produto.
- **dsa_mart_vendas_por_cliente:** total de itens comprados e valor gasto por cliente.
- **dsa_mart_vendas_por_mes:** vendas agregadas por mês, trimestre e ano.

As dimensões e a fato são materializadas como tabelas; os marts, como views.

## Estrutura do projeto

```
dbt-bigquery-pipeline/
├── scripts/
│   └── carrega_dados_bigquery.py    # ingestao dos CSVs para o BigQuery
├── models/
│   ├── sources.yml                  # definicao das fontes (dataset dsastaging)
│   ├── schema.yml                   # documentacao dos modelos dimensionais
│   ├── staging/                     # dimensoes e fato (esquema estrela)
│   │   ├── dim_clientes.sql
│   │   ├── dim_data.sql
│   │   ├── dim_localidades.sql
│   │   ├── dim_produtos.sql
│   │   └── fato_vendas.sql
│   └── marts/                       # visoes analiticas agregadas
│       ├── dsa_mart_vendas_por_categoria.sql
│       ├── dsa_mart_vendas_por_cliente.sql
│       └── dsa_mart_vendas_por_mes.sql
├── dbt_project.yml
└── README.md
```

## Como executar

### Pré-requisitos

- Projeto ativo no Google Cloud com BigQuery habilitado.
- Service account com permissão de leitura e escrita no BigQuery e o respectivo arquivo de chave JSON.
- Python 3.11 e dbt Core 1.8 com o adapter do BigQuery instalados.

### 1. Configurar credenciais

A autenticação é feita via service account. Defina o caminho da sua chave na variável de ambiente:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/caminho/para/sua-chave.json"
```

Configure também o perfil do dbt em `~/.dbt/profiles.yml` apontando para o seu projeto, dataset e chave.

### 2. Carregar os dados brutos

```bash
python scripts/carrega_dados_bigquery.py
```

O script cria o dataset de staging no BigQuery e carrega os cinco CSVs nas tabelas brutas.

### 3. Executar as transformações

```bash
dbt debug    # valida a conexao com o BigQuery
dbt run      # constroi dimensoes, fato e marts
dbt test     # executa os testes de qualidade dos dados
```

## Observações

Os dados utilizados são fictícios, gerados para fins de estudo de modelagem dimensional e transformação de dados com dbt sobre o BigQuery.
