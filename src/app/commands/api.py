"""stup api — Minimal FastAPI microservice scaffold."""

from app.utils import (
    check_uv,
    create_dirs,
    ensure_venv_exists,
    print_banner,
    print_done,
    run,
    write_file,
)

# ── Templates ────────────────────────────────────────────────────────

MAIN_PY = '''\
"""FastAPI microservice entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import health, v1
from middleware.auth import AuthMiddleware

app = FastAPI(
    title="My API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom auth middleware (optional — uncomment to enable)
# app.add_middleware(AuthMiddleware)

# Routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(v1.router, prefix="/api/v1", tags=["v1"])


@app.get("/")
async def root():
    return {"message": "Welcome to the API. Visit /docs for documentation."}
'''

HEALTH_ROUTER = '''\
"""Health check router."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    return {"status": "ok"}


@router.get("/ready")
async def readiness():
    return {"status": "ready"}
'''

V1_ROUTER = '''\
"""API v1 router."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Item(BaseModel):
    name: str
    description: str = ""
    price: float


# In-memory store (replace with database)
items: list[Item] = []


@router.get("/items")
async def list_items():
    return {"items": items}


@router.post("/items")
async def create_item(item: Item):
    items.append(item)
    return {"message": "Item created", "item": item}


@router.get("/items/{item_id}")
async def get_item(item_id: int):
    if 0 <= item_id < len(items):
        return {"item": items[item_id]}
    return {"error": "Item not found"}
'''

MODELS_INIT = '''\
"""Pydantic models / schemas."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class ErrorResponse(BaseModel):
    detail: str
'''

AUTH_MIDDLEWARE = '''\
"""Authentication middleware stub."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class AuthMiddleware(BaseHTTPMiddleware):
    """Simple API key authentication middleware.

    TODO: Replace with your preferred auth strategy (JWT, OAuth, etc.)
    """

    SKIP_PATHS = {"/", "/docs", "/redoc", "/openapi.json", "/health", "/health/ready"}

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.SKIP_PATHS:
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing X-API-Key header"},
            )

        # TODO: Validate api_key against your store
        # if not is_valid_key(api_key):
        #     return JSONResponse(status_code=403, content={"detail": "Invalid API key"})

        return await call_next(request)
'''


def run_command() -> None:
    """Scaffold a minimal FastAPI microservice."""
    print_banner("api", "Minimal FastAPI microservice with auth middleware")

    check_uv()
    ensure_venv_exists()

    # Install dependencies
    run("uv add fastapi uvicorn pydantic")

    # Create directory structure
    create_dirs("routers/v1", "routers/health", "models", "middleware")

    # Create files
    write_file("main.py", MAIN_PY)
    write_file("routers/__init__.py", "")
    write_file("routers/health/__init__.py", HEALTH_ROUTER)
    write_file("routers/v1/__init__.py", V1_ROUTER)
    write_file("models/__init__.py", MODELS_INIT)
    write_file("middleware/__init__.py", "")
    write_file("middleware/auth.py", AUTH_MIDDLEWARE)

    print_done()
