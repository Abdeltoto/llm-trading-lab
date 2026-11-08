# Matrice fonctionnelle (marketing / technique)

| Fonction | Bénéfice utilisateur | Implémentation |
|----------|---------------------|----------------|
| Bandeau SIMULATION | Confiance, conformité narrative | UI + API `simulation_banner` |
| Modes DEMO/BACKTEST/PAPER | Scénarios clairs | `TRADING_MODE` |
| Arène | Comparaison visuelle | `/arena`, lightweight-charts |
| Contrat JSON décision | Validation, audit | Pydantic `DecisionContract` |
| RiskEngine | Plafonds non contournables par le LLM | `backend/app/modules/risk` |
| Ledger Decimal | Comptabilité cohérente | `PortfolioState`, DB fills |
| Exécution T+1 open | Pas de look-ahead sur fill | `LocalCanonicalExecutionEngine` |
| Rapports HTML/JSON | Reproductibilité | `reports/generator.py` |
| Garde URLs ordre | Anti trading réel | `TradingUrlGuard` |
| Budget IA campagne | Coût visible | modèle `Campaign.ai_budget_usd` |

Utiliser cette matrice dans slides, issues « marketing », ou fiches produit interne.
