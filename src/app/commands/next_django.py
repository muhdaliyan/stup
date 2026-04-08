"""stup next-django — Next.js 14 + Django REST + JWT auth scaffold."""

from app.utils import (
    check_node,
    check_uv,
    create_dirs,
    ensure_venv_exists,
    print_banner,
    print_done,
    run,
    write_file,
)

# ── Templates ────────────────────────────────────────────────────────

ENV_FILE = '''\
# Django Backend
SECRET_KEY=change-me-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=7

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api
'''

JWT_SETTINGS = '''\
"""JWT authentication settings to add to Django settings.py.

Add this to your INSTALLED_APPS:
    'rest_framework',
    'rest_framework_simplejwt',

And add this REST_FRAMEWORK config:

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
"""
'''

BACKEND_URLS = '''\
"""Backend URL configuration with JWT auth endpoints."""

from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
'''

FRONTEND_API_CLIENT = '''\
import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
});

// Attach access token to every request
api.interceptors.request.use((config) => {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auto-refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      try {
        const refresh = localStorage.getItem("refresh_token");
        const { data } = await axios.post(`${API_URL}/token/refresh/`, { refresh });
        localStorage.setItem("access_token", data.access);
        original.headers.Authorization = `Bearer ${data.access}`;
        return api(original);
      } catch {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
'''


def run_command() -> None:
    """Scaffold a Next.js + Django REST + JWT project."""
    print_banner("next-django", "Next.js 14 + Django REST + JWT auth")

    check_uv()
    check_node()
    ensure_venv_exists()

    # ── Backend ──────────────────────────────────────────────────────
    create_dirs("backend")

    run("uv add django djangorestframework djangorestframework-simplejwt django-cors-headers")
    run("uv run django-admin startproject config backend/")

    write_file("backend/jwt_settings.py", JWT_SETTINGS)

    # Overwrite urls.py with JWT endpoints
    write_file("backend/config/urls.py", BACKEND_URLS)

    # ── Frontend ─────────────────────────────────────────────────────
    run("npx -y create-next-app@latest frontend --ts --tailwind --app --src-dir --eslint --no-turbopack --import-alias \"@/*\"")
    run("npm install axios jwt-decode", cwd="frontend")

    # API client with JWT interceptors
    create_dirs("frontend/src/lib")
    write_file("frontend/src/lib/api.ts", FRONTEND_API_CLIENT)

    # ── Root config ──────────────────────────────────────────────────
    write_file(".env", ENV_FILE)

    print_done()
