# Revue des dépôts de référence — LLM Trading Lab

*Date d’examen : 8 novembre 2026 (UTC). Les étoiles GitHub sont un indicateur de visibilité, pas de qualité.*

## Synthèse décisionnelle

| Projet | Décision | Moteur / rôle dans LLM Trading Lab |
|--------|----------|-------------------------------------|
| **NautilusTrader** | Adapter plus tard (interface prête) | Cible long terme pour simulation événementielle ; non installé en V1 |
| **Simulateur local canonique** | **Adopter** | Moteur V1 derrière `ExecutionEngine` |
| **QuantConnect Lean** | Écarter (install) / référence | Modèle d’événements de marché ; stack C#/Python lourde |
| **Microsoft Qlib** | Intégration ultérieure | Pipeline recherche quanti ; pas sur chemin critique V1 |
| **TradingAgents** | S’inspirer (orchestration) | Architecture multi-agents (expérience secondaire) sans import du graphe |
| **FinRL** | Hors chemin critique | RL facultatif |
| **Alpaca skills + Paper API** | Guider connecteur optionnel | Validation paper isolée, étape 5 |

## Dépôts examinés

### nautechsystems/nautilus_trader

- **Rôle** : moteur de trading événementiel, backtest et live, cœur Rust + bindings Python.
- **Licence** : LGPL-3.0 (obligations de partage si modification/liaison selon usage).
- **Maintenance** : poussé le 2026-11-08 ; ~31 370 étoiles au 2026-11-08.
- **Compatibilité** : cible principale Linux/macOS ; Windows natif limité. Docker/Linux/WSL2 viable.
- **Décision** : ne pas embarquer en V1 (poids, LGPL, cycle d’intégration). L’interface `ExecutionEngine` permet un adaptateur `NautilusExecutionAdapter` sans changer l’API.

### QuantConnect/Lean

- **Rôle** : moteur algorithmique complet (actions, options, etc.).
- **Licence** : Apache-2.0.
- **Maintenance** : poussé le 2026-11-06 ; ~22 451 étoiles au 2026-11-08.
- **Décision** : écarter comme dépendance ; conserver comme référence pour ordre des événements et conventions de données.

### microsoft/qlib

- **Rôle** : plateforme de recherche quanti orientée ML.
- **Licence** : MIT.
- **Maintenance** : poussé le 2026-11-04 ; ~50 132 étoiles au 2026-11-08.
- **Décision** : intégration ultérieure (features, benchmarks quanti) via export Parquet.

### TauricResearch/TradingAgents

- **Rôle** : cadre multi-agents LLM pour décisions de trading.
- **Licence** : Apache-2.0.
- **Maintenance** : poussé le 2026-11-04 ; ~121 346 étoiles au 2026-11-08.
- **Décision** : inspirer les rôles (analyste technique, actualités, macro, synthèse) pour l’architecture B ; V1 = architecture A uniquement.

### AI4Finance-Foundation/FinRL

- **Rôle** : reinforcement learning pour finance.
- **Licence** : MIT.
- **Maintenance** : poussé le 2026-11-03 ; ~17 020 étoiles au 2026-11-08.
- **Décision** : hors chemin critique.

### alpacahq/alpaca-skills

- **Rôle** : skills officiels (dont `trading-api/paper-trading`, `backtest`, `paper-trading-cli`).
- **Usage** : guide pour connecteur **paper uniquement**, comptes isolés par concurrent, pas de mélange avec le simulateur local dans un même classement.
- **Référence** : [Alpaca Paper Trading](https://docs.alpaca.markets/docs/paper-trading) — simulateur externe, limites de flux et d’exécution distinctes du moteur local.

## Moteur retenu pour la V1

**Simulateur local canonique** (`LocalCanonicalExecutionEngine`) :

- Règles identiques pour tous les concurrents d’un tournoi donné.
- Paramètres de spread, commission, slippage et latence déclarés (`docs/execution-assumptions.md`).
- Exécution au **open** de la séance suivant la décision (convention prudente sans bid/ask).
- Aucune URL d’ordre réel ; garde `TRADING_MODE` et liste blanche d’hôtes.

Adaptateurs futurs : `AlpacaPaperExecutionAdapter` (comptes paper séparés), `NautilusExecutionAdapter` (worker Linux).

## Compétences applicatives internes (non skills tiers)

1. **Intégrité temporelle des données** — `available_at` / pas de fuite d’information future.
2. **Évaluation LLM** — contrat JSON, journalisation, coûts, échecs conservés.
3. **Comptabilité de portefeuille** — registre transactionnel `Decimal`, coût de revient, PnL.
4. **Risque déterministe** — `RiskEngine` indépendant du modèle.
5. **Exécution simulée** — fills, frais, idempotence, pas de fill à la clôture de décision.
6. **Analyse statistique** — benchmarks alignés, ratios avec conventions explicites.

## Stack retenue

- Frontend : React 18, TypeScript, Vite, Tailwind ; graphiques **lightweight-charts** (Apache-2.0, attribution TradingView).
- Backend : Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2, Alembic.
- Données : PostgreSQL 16 ; archives Parquet (`data/archives/`).
- Worker : processus Python (Celery + Redis optionnel en prod locale).
- CI : GitHub Actions (pytest, lint frontend).

## Versions étudiées (API GitHub, branche par défaut)

| Dépôt | Branche par défaut | Commit HEAD (approx.) |
|-------|-------------------|------------------------|
| nautilus_trader | develop | non épinglé — suivre releases PyPI pour adaptateur |
| qlib | main | non épinglé |
| Lean | master | non épinglé |
| TradingAgents | main | non épinglé |
| FinRL | master | non épinglé |

Le commit logiciel du lab est enregistré par campagne via variable d’environnement `GIT_COMMIT` / `APP_VERSION` au runtime.
