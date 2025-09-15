## Data Warehouse enxuto — Rede de Supermercados (Lakehouse barato)

### Problema de negócio
- Consolidar vendas de +300 lojas físicas e e-commerce para responder:
  - Receita total e por canal/loja/categoria
  - Impacto de promoções na receita e margem
  - Margem de lucro e evolução temporal

### Decisões (v1 local-first, baixo custo)
- Camadas: bronze (bruto) → prata (limpo) → ouro (marts analíticos)
- Formato: Parquet particionado por data; catálogo leve via metadados no repositório
- Engine: DuckDB (SQL) para transformação local e consultas analíticas
- Orquestração: scripts/Makefile simples (Airflow em fase futura)
- Qualidade: checks mínimos (schema, nulos, domínios) na ingestão
- Versionamento & DX: Git, pre-commit/commitizen, docs no `docs/`

### Arquitetura (v1)
```mermaid
flowchart LR
    subgraph Sources[Fontes]
      DB[(PostgreSQL lojas)]
      API[(API Ecommerce)]
      XLS[(Excel catálogo)]
    end

    DB -->|extract| BRZ[Bronze Parquet]
    API -->|extract| BRZ
    XLS -->|extract| BRZ

    BRZ -->|DuckDB SQL| SILVER[Prata (limpeza/normalização)]
    SILVER -->|modelagem dimensional| GOLD[Ouro (fatos e dimensões)]
    GOLD --> BI[BI/Dashboards]

    classDef stor fill:#eef,stroke:#99f;
    class BRZ,SILVER,GOLD stor;
```

### Trade-offs
- Simplicidade e custo ≫ alta escala: DuckDB+Parquet elimina infra e é rápido em 1–50 GB locais; perde em concorrência multiusuário e workloads >100s GB
- Catálogo leve ≫ metastore: menor acoplamento, porém menos governança; futuro: Glue/Unity/DBT docs
- Orquestração manual ≫ Airflow: maior velocidade para v1; menos observabilidade e SLAs

### Estimativa de custo
- Local (v1): ~R$0 (armazenamento local + DuckDB)
- Futuro AWS mínimo (opcional):
  - S3: R$10–40/mês (100–500 GB, dependente de região e acessos)
  - EC2 t4g.small ou Fargate esporádico: R$30–120/mês
  - RDS Postgres (dev): R$60–180/mês
  - Observação: custos variam por uso, região e transferências

### Roadmap de evolução
- v2: Catálogo (dbt docs) e testes (dbt tests/Great Expectations)
- v3: Orquestração com Airflow, backfills e SLAs
- v4: Lake no S3/MinIO + particionamento por dt e país; Delta/iceberg opcional
- v5: Marts consumidos por BI (Metabase/Superset) e métricas padronizadas