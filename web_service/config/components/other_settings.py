import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get("DJANGO_DEBUG", False) == "True"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(",")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
