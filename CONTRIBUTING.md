# Contribuer

Merci d’enrichir un projet **recherche / éducation**, pas un produit de conseil financier.

## Avant de coder

1. Lire [docs/methodology.md](docs/methodology.md) et [docs/marketing/disclaimer.md](docs/marketing/disclaimer.md).
2. Vérifier que votre changement ne réintroduit **aucun** chemin vers trading réel.
3. Ajouter ou mettre à jour des tests pour la logique métier touchée (`backend/tests/`).

## Environnement

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
python -m scripts.generate_demo_parquet
$env:PYTHONPATH="."; python -m pytest -q tests
```

## Style

- Python : types explicites sur API publiques, `Decimal` pour la comptabilité.
- UI : français par défaut, accessibilité (contraste, états vides).
- Commits : message en anglais ou français, impératif court (« fix », « docs », « feat »).

## Pull requests

- Décrire le mode concerné (DEMO / BACKTEST / PAPER_FORWARD).
- Mentionner les limites connues et le moteur d’exécution (`local_canonical` vs Alpaca paper).
- CI doit rester verte (backend pytest + frontend `npm run lint`).

## Ce que nous n’acceptons pas

- Boutons ou routes de passage en réel.
- Clés ou secrets dans le dépôt.
- Classements mélangeant deux moteurs d’exécution.
- Suppression d’échecs LLM pour « améliorer » un score.
