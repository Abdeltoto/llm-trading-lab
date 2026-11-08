# Pitch (30 s, 2 min, README)

## 30 secondes

« LLM Trading Lab est une plateforme open source qui fait s’affronter des modèles IA sur une **même campagne simulée** : mêmes données, mêmes règles de risque, même budget API. Vous voyez rendement, drawdown, incidents et **coût réel de l’IA** — pas un trading réel. Idéal pour des expériences reproductibles en classe ou en R&D. »

## 2 minutes

1. **Contexte** — Les LLM prétendent « trader » ; les démos manquent d’audit et mélangent données, frais et coût inférence.
2. **Solution** — Monolithe modulaire (FastAPI + React) avec journal transactionnel, `RiskEngine`, contrat JSON de décision, arène multi-concurrents.
3. **Modes** — DEMO sans clé, BACKTEST étiqueté exploratoire, PAPER_FORWARD pour le suivi prospectif.
4. **Sécurité produit** — Pas de bouton live ; gardes sur URLs d’ordre ; concurrents isolés.
5. **Open source** — MIT, Docker, tests métier, doc méthodologique complète.
6. **Suite** — Brancher vos clés LLM, lancer une campagne 8 semaines, comparer architecture simple vs multi-agents (roadmap).

## Anglais (GitHub international)

**LLM Trading Lab** is an open research stack to compare LLM models on **controlled, fully simulated** portfolio decisions—with auditable logs, deterministic risk checks, and separate tracking of **fictional PnL vs real API spend**. No live trading. Demo runs offline with deterministic agents.
