# Guide de démarrage

## Prérequis

- Docker **ou** Python 3.12 + Node 20
- Windows, WSL2 ou Linux

## Chemin le plus rapide (Docker)

```powershell
git clone https://github.com/<VOTRE_ORG>/llm-trading-lab.git
cd llm-trading-lab
copy .env.example .env
docker compose up --build
```

| Service | URL |
|---------|-----|
| Interface | http://localhost:5180 |
| API OpenAPI | http://localhost:8808/docs |
| Auth | `demo` / `demo` |

## Chemin développeur (local)

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
python -m scripts.generate_demo_parquet
$env:PYTHONPATH="."
$env:DATABASE_URL="sqlite+pysqlite:///c:/chemin/vers/data/lab.db"
$env:TRADING_MODE="DEMO"
python -c "from app.db import Base, engine; Base.metadata.create_all(bind=engine)"
python -m scripts.seed_demo
.\.venv\Scripts\uvicorn app.main:app --host 127.0.0.1 --port 8808
```

### Frontend

```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5180
```

## Premier parcours utilisateur

1. Ouvrir **Campagnes** → *Créer campagne DEMO* (ou utiliser le seed).
2. *Exécuter un pas* → génère décisions + ordres simulés.
3. **Arène** → courbes et classement.
4. **Rapports** → télécharger JSON ou HTML.

## Dépannage

| Symptôme | Action |
|----------|--------|
| `ERR_CONNECTION_REFUSED` | Démarrer API (8808) et UI (5180) |
| Proxy Vite `/api` en échec | Vérifier qu’uvicorn tourne sur 8808 |
| Données manquantes | `python -m scripts.generate_demo_parquet` |

## Aller plus loin

- [Configuration LLM](../README.md#configuration-llm-et-alpaca-paper)
- [Méthodologie](methodology.md)
- [Publication GitHub](marketing/github-launch.md)
