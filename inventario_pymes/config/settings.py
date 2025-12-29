"""
Django settings for config project.
Preparado para PRODUCCIÓN (venta / nube)
"""

from pathlib import Path
import os

# =========================================================
# BASE
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# SEGURIDAD
# =========================================================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-dev-key-solo-para-local"
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1"
).split(",")

# Necesario para HTTPS en Render / Railway / etc.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# =========================================================
# APPS
# =========================================================

INSTALLED_APPS = [
    # Django base
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Django REST
    "rest_framework",
    "rest_framework.authtoken",

    # Filtros
    "django_filters",

    # Swagger
    "drf_yasg",

    # CORS
    "corsheaders",

    # App principal
    "inventario",
]

# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =========================================================
# URLS
# =========================================================

ROOT_URLCONF = "config.urls"

# =========================================================
# TEMPLATES
# =========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# =========================================================
# WSGI
# =========================================================

WSGI_APPLICATION = "config.wsgi.application"

# =========================================================
# BASE DE DATOS
# =========================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# =========================================================
# DRF / SEGURIDAD
# =========================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}

# =========================================================
# CORS
# =========================================================

CORS_ALLOW_ALL_ORIGINS = DEBUG  # solo en desarrollo

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_HEADERS = ["*"]
CORS_ALLOW_METHODS = ["*"]

# =========================================================
# INTERNACIONALIZACIÓN
# =========================================================

LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# =========================================================
# ESTÁTICOS
# =========================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# =========================================================
# DEFAULT
# =========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
