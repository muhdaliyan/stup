# arrange

> 🚀 Scaffold production-ready project structures in seconds. Install once, scaffold forever.

```bash
pip install arrange
```

## Foundation Commands

### `arrange uv`

Bootstraps a complete uv Python project. Run this first before any template.

```bash
$ arrange uv
```

- `uv init` — creates pyproject.toml and project skeleton
- `uv python pin 3.12` — pins Python version
- `uv venv` — creates virtual environment
- Prints activation command (cross-platform)

### `arrange activate`

Smart cross-platform venv activator — detects your shell and prints the right command.

- **Windows PowerShell:** `.venv\Scripts\Activate.ps1`
- **Linux/Mac bash/zsh:** `source .venv/bin/activate`

---

## Template Commands

Each template builds on top of `arrange uv`. Run `arrange uv` first, then pick your template.

### `arrange react-fastapi`

| | |
|---|---|
| **Description** | Full-stack web app — React frontend + FastAPI backend with Docker Compose and CORS pre-configured |
| **Stack** | Python + JavaScript (Vite, React, Tailwind, FastAPI, Alembic) |
| **Installs** | `uv add fastapi uvicorn alembic` \| `npm install react tailwindcss vite` |
| **Structure** | `frontend/` `backend/` `docker-compose.yml` `.env` |

### `arrange notebook`

| | |
|---|---|
| **Description** | Data science workspace with Jupyter notebooks, uv-managed deps, kernel auto-registered |
| **Stack** | Python + Jupyter |
| **Installs** | `uv add ipykernel pandas numpy matplotlib` |
| **Structure** | `notebooks/` `data/raw/` `data/processed/` |

### `arrange mern`

| | |
|---|---|
| **Description** | MongoDB + Express + React + Node full-stack app with concurrently dev script |
| **Stack** | JavaScript (MongoDB, Express, React, Node) |
| **Installs** | `npm install express mongoose dotenv` \| `npm install react react-router-dom axios` |
| **Structure** | `client/` `server/` `.env` (PORT, MONGO_URI) |

### `arrange mean`

| | |
|---|---|
| **Description** | MongoDB + Express + Angular + Node — same as MERN but with Angular 17 + TypeScript |
| **Stack** | JavaScript + TypeScript (MongoDB, Express, Angular) |
| **Installs** | `npm install @angular/cli express mongoose cors` |
| **Structure** | `client/` (Angular) `server/` (Express) `proxy.conf.json` |

### `arrange django`

| | |
|---|---|
| **Description** | Production-ready Django + DRF + Celery + Redis + PostgreSQL setup with python-decouple |
| **Stack** | Python (Django, DRF, Celery, Redis, PostgreSQL) |
| **Installs** | `uv add django djangorestframework celery redis python-decouple` |
| **Structure** | `config/` `apps/users/` `apps/api/` `tasks/` `.env` |

### `arrange next-django`

| | |
|---|---|
| **Description** | Next.js 14 frontend + Django REST backend with JWT auth pre-wired |
| **Stack** | Python + JavaScript (Next.js, DRF, SimpleJWT, axios) |
| **Installs** | `uv add djangorestframework-simplejwt` \| `npm install next axios jwt-decode` |
| **Structure** | `frontend/` (Next.js) `backend/` (Django) `.env` |

### `arrange ml`

| | |
|---|---|
| **Description** | ML project scaffold with experiment tracking, model versioning, and MLflow stub |
| **Stack** | Python (scikit-learn, PyTorch, MLflow) |
| **Installs** | `uv add scikit-learn torch mlflow` |
| **Structure** | `data/` `models/` `experiments/runs/` `experiments/configs/` |

### `arrange agent`

| | |
|---|---|
| **Description** | LangGraph AI agent with tool stubs, memory/checkpointing, and Ollama config |
| **Stack** | Python (LangGraph, LangChain, Ollama) |
| **Installs** | `uv add langgraph langchain-community` |
| **Structure** | `agent.py` `tools/` `memory/` `.env` (OLLAMA_BASE_URL, model) |

### `arrange scraper`

| | |
|---|---|
| **Description** | Web scraping project with Playwright, BeautifulSoup, pandas output pipeline and scheduler |
| **Stack** | Python (Playwright, BeautifulSoup4, pandas) |
| **Installs** | `uv add playwright beautifulsoup4 pandas schedule` + `playwright install chromium` |
| **Structure** | `spider.py` `pipeline.py` `data/raw/` `data/cleaned/` |

### `arrange cli`

| | |
|---|---|
| **Description** | PyPI-ready Python CLI package with Typer + Rich, entry_points wired in pyproject.toml |
| **Stack** | Python (Typer, Rich) |
| **Installs** | `uv add typer rich` |
| **Structure** | `src/<project>/` `commands/` `pyproject.toml` `README.md` |

### `arrange api`

| | |
|---|---|
| **Description** | Minimal FastAPI microservice with auth middleware stub and OpenAPI docs at /docs |
| **Stack** | Python (FastAPI, Pydantic, uvicorn) |
| **Installs** | `uv add fastapi uvicorn pydantic` |
| **Structure** | `main.py` `routers/v1/` `routers/health/` `models/` `middleware/` |

### `arrange saas`

| | |
|---|---|
| **Description** | Full SaaS boilerplate — auth, Stripe billing, Celery workers, Redis, Postgres, all Dockerized |
| **Stack** | Python + JavaScript (Django, React, Stripe, Celery, Redis) |
| **Installs** | `uv add django stripe celery redis` \| `npm install @stripe/stripe-js` |
| **Structure** | `backend/auth/` `backend/billing/` `backend/api/` `frontend/` `docker-compose.yml` |

### `arrange docs`

| | |
|---|---|
| **Description** | Adds MkDocs + Material theme + auto-docstring config to any existing project |
| **Stack** | Python (MkDocs, Material theme) |
| **Installs** | `uv add mkdocs mkdocs-material` |
| **Structure** | `docs/` `mkdocs.yml` |

### `arrange test`

| | |
|---|---|
| **Description** | Scaffolds a full pytest suite — conftest, fixtures, coverage config |
| **Stack** | Python (pytest, coverage) |
| **Installs** | `uv add pytest pytest-cov` |
| **Structure** | `tests/` `conftest.py` `fixtures/` `.coveragerc` |

---

## Quick Reference

| Command | Stack | Use Case |
|---------|-------|----------|
| `arrange uv` | Python | Start any Python project |
| `arrange activate` | Python | Activate venv cross-platform |
| `arrange react-fastapi` | Py + JS | Full-stack web app |
| `arrange notebook` | Python | Data science / Jupyter |
| `arrange mern` | JS | MongoDB + React stack |
| `arrange mean` | JS + TS | MongoDB + Angular stack |
| `arrange django` | Python | Full Django + Celery API |
| `arrange next-django` | Py + JS | Next.js + Django + JWT |
| `arrange ml` | Python | ML project + MLflow |
| `arrange agent` | Python | LangGraph AI agent |
| `arrange scraper` | Python | Web scraping pipeline |
| `arrange cli` | Python | PyPI-ready CLI package |
| `arrange api` | Python | FastAPI microservice |
| `arrange saas` | Py + JS | Full SaaS boilerplate |
| `arrange docs` | Python | MkDocs documentation |
| `arrange test` | Python | pytest suite scaffold |

---

## Development

```bash
git clone https://github.com/teeon/arrange.git
cd arrange
uv venv
uv pip install -e ".[dev]"
arrange --help
```

## License

MIT
