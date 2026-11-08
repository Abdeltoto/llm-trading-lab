# Publier sur GitHub (dépôt public)

## Checklist avant `git push`

- [ ] `.env` **non** suivi (`git status` propre)
- [ ] `docs/assets/og-social-preview.jpg` présent
- [ ] README à jour (ports 5180 / 8808)
- [ ] LICENSE, SECURITY.md, CONTRIBUTING.md présents
- [ ] Aucune clé dans l’historique (`git log -p` si doute)

## Créer le dépôt public

### Option A — GitHub CLI

```powershell
cd c:\project\traiding
git init -b main
git add -A
git commit -m "docs: marketing kit et publication initiale LLM Trading Lab"
gh repo create llm-trading-lab --public --source=. --remote=origin --push
```

Renommez `llm-trading-lab` si le nom est pris.

### Option B — Interface web

1. GitHub → New repository → **Public** → sans README (déjà local).
2. `git remote add origin https://github.com/<USER>/llm-trading-lab.git`
3. `git push -u origin main`

## Réglages repo recommandés

| Réglage | Valeur |
|---------|--------|
| Description | Open research platform comparing LLMs on simulated trading (fictive funds only) |
| Topics | `llm`, `trading`, `simulation`, `fastapi`, `react`, `quantitative-finance`, `paper-trading` |
| Social preview | Upload `docs/assets/og-social-preview.jpg` |
| About | Website vide ou lien doc Pages si activé |
| Security | Activer Dependabot / Secret scanning |

## GitHub Pages (optionnel)

Héberger la doc marketing + méthodo :

```powershell
# Exemple : copier docs/ vers branche gh-pages ou utiliser mkdocs ultérieurement
```

V1 : le README suffit pour le lancement.

## Annonce (modèle)

**Titre :** LLM Trading Lab — compare LLM models on auditable simulated trading

**Corps :**

> Open-source lab to run controlled arena experiments: same data, same risk rules, same decision time, API budget caps. DEMO runs without paid keys. Not investment advice. MIT.

Liens : README, disclaimer, `docker compose up`.

## Après publication

- Pin une issue « Roadmap » pointant vers [roadmap.md](roadmap.md)
- Label `good first issue` sur tâches doc/tests
- Ne pas activer Discussions sans modération légère
