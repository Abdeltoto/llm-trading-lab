# Sécurité

## Périmètre

LLM Trading Lab est un **logiciel de recherche** en environnement **simulé** (argent fictif). Il n’est pas conçu pour exécuter des ordres réels.

## Signaler une vulnérabilité

Si vous découvrez un problème de sécurité (fuite de secrets, contournement de garde-fous trading, injection via contenus non fiables, etc.) :

1. **Ne pas** ouvrir d’issue publique avec des détails exploitables.
2. Envoyer un rapport via les canaux de contact du dépôt GitHub (Security Advisory si activé) ou par issue privée si vous n’avez pas d’autre contact.
3. Inclure : version, mode (`TRADING_MODE`), étapes de reproduction, impact estimé.

Nous visons un accusé de réception sous **72 h** et une correction prioritaire pour tout contournement permettant le trading réel ou l’exfiltration de clés.

## Bonnes pratiques déploiement

- Ne jamais commiter `.env`, clés API, ni journaux contenant des secrets.
- Activer TLS pour toute exposition réseau.
- Changer `SECRET_KEY`, `DEMO_PASSWORD` en production.
- Garder `BLOCK_REAL_TRADING=true` sauf audit explicite du connecteur paper isolé.
- Budgets et rate limits LLM activés côté serveur uniquement.

## Données et confiance

Les textes ingérés (actualités, flux) sont **non fiables** : aucune instruction embarquée ne doit modifier les règles métier ni exécuter du code.
