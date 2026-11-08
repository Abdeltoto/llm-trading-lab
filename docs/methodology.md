# Méthodologie — LLM Trading Lab

## Question de recherche

Dans des conditions contrôlées (mêmes données, mêmes règles, même instant de décision, budget IA plafonné), quels modèles et architectures produisent les meilleures décisions **après** prise en compte du risque, des frais simulés et du coût API ?

## Modes

| Mode | Données | LLM | Exécution |
|------|---------|-----|-----------|
| `DEMO` | Synthétiques, seed fixe | Agents déterministes (zéro coût) | Simulateur local |
| `BACKTEST` | Historique figé, horloge simulée | Enregistré ou live selon config | Simulateur local |
| `PAPER_FORWARD` | Flux archivés au collecte | Live configurable | Local **ou** Alpaca Paper (jamais mélangés dans un classement) |

## Campagne par défaut (modifiable)

- Capital : **100 000 USD fictifs** par concurrent.
- Durée prospective cible : **8 semaines** (non exécutée automatiquement à l’installation).
- Univers V1 : SPY, QQQ, IWM, DIA, TLT, GLD.
- Long only, pas de levier ; max **6** positions, **25 %** max par instrument.
- Décisions sur **clôtures complètes** ; exécution à la **séance suivante** (open).
- Budget IA campagne par défaut : **50 USD** (affiché, plafonné).

## Expériences

- **Principale** : même prompt, même paquet d’information, même architecture A (poids cibles), même moteur.
- **Secondaire** (ultérieur) : architecture B multi-agents, hors classement principal.
- Changement de prompt ou de modèle → **nouvelle version** d’expérience.

## Biais et limites

- Les backtests LLM sont **exploratoires** (connaissances paramétriques des modèles).
- Huit semaines ne permettent **pas** d’inférer une supériorité durable.
- Données téléchargées aujourd’hui sans historique de disponibilité → signaler ou désactiver la modalité.

## Références de performance

- Cash (0 %).
- SPY buy-and-hold (même calendrier et conventions de rendement total sur séries ajustées démo).
- Panier équipondéré de l’univers.
- Stratégie déterministe documentée (`DeterministicRotateStrategy` en DEMO).

## Séparation des coûts

- **PnL portefeuille** (fictif) et **coût API réel** affichés séparément.
- Classement filtrable : rendement, drawdown, excès, coût, fiabilité (incidents).
