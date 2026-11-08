# Intégrité des données

## Horodatage

Chaque artefact porte lorsque pertinent :

- `event_time` — instant de l’événement de marché.
- `published_at` — publication (actualités, macro).
- `received_at` — réception par le connecteur.
- `available_at` — **premier instant où une décision peut lire l’information**.

Une décision à `as_of` ne voit que les enregistrements avec `available_at <= as_of`.

## Couches

1. **Brut** — téléchargements / flux paper archivés.
2. **Transformé** — ajustements corporate (splits, symboles) documentés.
3. **Features** — indicateurs calculés par le code (jamais inventés par le LLM).
4. **Snapshots** — paquets hashés servis au modèle (`data_snapshot_hash`).

## DEMO / BACKTEST

- DEMO : série générée avec calendrier US simplifié (jours ouvrés), sans fuite (snapshots construits à `as_of`).
- BACKTEST : navigation « présent » interdite ; outils actualité temps réel désactivés.

## Conventions prix

- **Exécution** : prix non ajustés (open du jour d’exécution).
- **Analytique / benchmarks** : séries **total return** démo cohérentes avec les mêmes facteurs d’ajustement synthétiques.
- Dividendes : enregistrés au registre ; pas de double comptage avec prix ajustés analytiques.

## Qualité

- Trous, jours fériés : calendrier `pandas_market_calendars` (NYSE) en modes non-DEMO lorsque activé.
- Fraîcheur : `RiskEngine` rejette si dernière barre trop ancienne vs `as_of`.

## Survivance

- Univers V1 = ETF liquides (biais réduit). Extension actions : nécessite historique de constituants — non activé en V1.
