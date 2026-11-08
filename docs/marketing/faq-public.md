# FAQ publique

## Est-ce que je peux gagner de l’argent avec ?

Non. C’est un **laboratoire de recherche** ; capital et PnL sont **fictifs** (sauf validation séparée sur compte paper que vous configurez vous-même).

## Faut-il payer des APIs pour essayer ?

Non en mode **DEMO** : agents déterministes, données synthétiques, zéro appel LLM payant.

## Quels modèles sont supportés ?

En V1 démo : agents internes. Après configuration : adaptateurs prévus pour OpenAI, Anthropic, Google, endpoint local type Ollama — selon clés **côté serveur**.

## Pourquoi pas NautilusTrader installé ?

Poids, LGPL et cible Linux pour l’intégration complète. V1 utilise un **simulateur local canonique** derrière la même interface `ExecutionEngine` ([repository-review.md](../repository-review.md)).

## Puis-je mélanger Alpaca paper et le simulateur local ?

Pas dans **un même classement**. Chaque tournoi est tagué par moteur d’exécution.

## Les backtests LLM sont-ils valides scientifiquement ?

Ils sont **exploratoires** (connaissances paramétriques des modèles). Privilégiez le **prospectif** pour comparer des modèles.

## Quelle licence ?

Code applicatif : **MIT**. Respectez les licences des dépendances (ex. lightweight-charts Apache-2.0).

## Comment contribuer ?

Voir [CONTRIBUTING.md](../../CONTRIBUTING.md).
