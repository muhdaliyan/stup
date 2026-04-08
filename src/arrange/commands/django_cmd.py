"""arrange django — Django + DRF + Celery + Redis + PostgreSQL scaffold."""

from arrange.utils import (
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
# Django
SECRET_KEY=change-me-to-a-real-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL)
DB_NAME=myapp
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Redis / Celery
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
'''

CELERY_APP = '''\
"""Celery application configuration."""

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
'''

CONFIG_INIT = '''\
"""Config package."""

from .celery import app as celery_app

__all__ = ("celery_app",)
'''

SAMPLE_TASK = '''\
"""Example Celery tasks."""

from config.celery import app


@app.task
def example_task(x, y):
    """Add two numbers — example async task."""
    return x + y
'''

USERS_SERIALIZERS = '''\
"""User serializers."""

from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined"]
        read_only_fields = ["id", "date_joined"]
'''

USERS_VIEWS = '''\
"""User API views."""

from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
'''

API_URLS = '''\
"""API URL configuration."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
'''


def run_command() -> None:
    """Scaffold a Django + DRF + Celery project."""
    print_banner("django", "Django + DRF + Celery + Redis + PostgreSQL")

    check_uv()
    ensure_venv_exists()

    # Install dependencies
    run("uv add django djangorestframework celery redis python-decouple psycopg2-binary")

    # Create Django project
    run("uv run django-admin startproject config .")

    # Create apps
    create_dirs(
        "apps/users",
        "apps/api",
        "tasks",
    )

    # Create app files
    run("uv run python manage.py startapp users apps/users")
    write_file("apps/users/serializers.py", USERS_SERIALIZERS)
    write_file("apps/users/views.py", USERS_VIEWS)
    write_file("apps/api/urls.py", API_URLS)
    write_file("apps/api/__init__.py", "")

    # Celery config
    write_file("config/celery.py", CELERY_APP)
    write_file("tasks/example.py", SAMPLE_TASK)
    write_file("tasks/__init__.py", "")

    # Update config/__init__.py to load celery
    write_file("config/__init__.py", CONFIG_INIT)

    # Environment file
    write_file(".env", ENV_FILE)

    print_done()
