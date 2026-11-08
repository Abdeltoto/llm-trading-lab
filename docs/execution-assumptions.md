# Hypothèses d’exécution simulée (moteur local canonique)

## Principe

Les décisions utilisent la **clôture** du jour `T`. Les ordres sont admis à l’**open** du jour ouvré suivant `T+1` (après l’heure effective de décision).

**Interdit** : fill au prix de clôture de `T` pour une décision prise après cette clôture.

## Sans carnet bid/ask

Hypothèse par défaut (configurable via `EXECUTION_*`) :

| Paramètre | Défaut DEMO | Étiquette |
|-----------|-------------|-----------|
| Commission | 0 USD + 0.1 bps notionnel | `estimation` |
| Spread demi | 1 bp sur open | `estimation` |
| Slippage | 2 bp directionnel sur open | `estimation` |
| Latence | Exécution à l’open uniquement | déterministe |

Achat : `fill_price = open * (1 + spread + slippage)`. Vente : `fill_price = open * (1 - spread - slippage)`.

## Types d’ordres V1

- **Market on open** du jour d’exécution (quantités entières, pas de fraction d’action).
- Pas de vente à découvert ; ventes limitées aux quantités détenues.

## OHLC seulement

Pas de chemin intrabar : une seule exécution par symbole et par jour d’exécution au prix open ajusté par hypothèses ci-dessus.

## Moteurs distincts

- Classements **tagués** `execution_engine=local_canonical` ou `alpaca_paper`.
- Ne jamais agréger les performances de deux moteurs dans le même tableau de tournoi.

## Sécurité d’exécution

- `TRADING_MODE` ∈ {`DEMO`, `BACKTEST`, `PAPER_FORWARD`}.
- Hôtes d’**ordre** : liste blanche (`paper-api.alpaca.markets` si connecteur Alpaca activé explicitement).
- Blocage de tout hôte de trading **réel** (ex. `api.alpaca.markets` sans flag paper, courtiers live).
