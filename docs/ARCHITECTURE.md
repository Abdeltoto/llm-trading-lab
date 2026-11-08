# Architecture

```mermaid
flowchart TB
  subgraph client [Navigateur]
    UI[React Vite FR]
  end
  subgraph api [API FastAPI]
    R[Routes /api/v1]
    A[Auth Basic]
  end
  subgraph core [Modules métier]
    DP[DataProvider]
    LLM[LLMProvider]
    ST[Strategy / Agents]
    RK[RiskEngine]
    EX[ExecutionEngine]
    LD[PortfolioLedger]
    ER[ExperimentRunner]
    AN[Analytics / Reports]
  end
  subgraph data [Persistance]
    PG[(PostgreSQL)]
    PQ[Parquet archives]
  end
  UI --> R
  R --> A
  R --> ER
  ER --> DP
  ER --> LLM
  ER --> ST
  ER --> RK
  ER --> EX
  EX --> LD
  ER --> LD
  LD --> PG
  DP --> PQ
  AN --> PG
```

## Services nommés

| Service | Rôle |
|---------|------|
| `DataProvider` | Barres, snapshots `available_at`, hash paquet |
| `LLMProvider` | Inférence structurée (DEMO = déterministe) |
| `Strategy` | Architecture A : poids cibles |
| `RiskEngine` | Validation indépendante |
| `ExecutionEngine` | Fills simulés (`local_canonical`) |
| `PortfolioLedger` | Cash, positions, frais |
| `ExperimentRunner` | Cycle décision → ordres → équité |

## Flux décision (résumé)

1. Construire snapshot **≤ as_of**.
2. Obtenir `DecisionContract` (ou échec journalisé).
3. `RiskEngine.validate_decision`.
4. Si OK : cibles → quantités → ordres idempotents → fills T+1.
5. Snapshot équité + rapport.

## Déploiement

- **Docker Compose** : `api`, `worker`, `postgres`, `redis`, `frontend` (nginx).
- Ports hôte par défaut : UI **5180**, API **8808**.

Voir [repository-review.md](repository-review.md) pour les choix de moteur et dépendances externes.
