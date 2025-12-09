"""
Django settings for config project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------
# SEGURIDAD
# ---------------------------------------------------------

SECRET_KEY = 'django-insecure--c7pmeu1fk79x-t*1e0k_^7_b$(@s66o@bdn*853a@4g4teg+-'
DEBUG = True
ALLOWED_HOSTS = ["*"]

# ---------------------------------------------------------
# APPS
# ---------------------------------------------------------

INSTALLED_APPS = [
    # Django base
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django REST Framework
    'rest_framework',
    'rest_framework.authtoken',

    # Filtros
    'django_filters',

    # Documentación Swagger
    'drf_yasg',

    # CORS para conectar React
    'corsheaders',

    # Tu app
    'inventario',
]

# ---------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',   # CORS arriba
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------------------------------------
# URLS PRINCIPALES
# ---------------------------------------------------------

ROOT_URLCONF = 'config.urls'

# ---------------------------------------------------------
# TEMPLATES (REQUERIDO PARA ADMIN)
# ---------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],   # Si usas templates futuros, aquí van
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ---------------------------------------------------------
# WSGI
# ---------------------------------------------------------

WSGI_APPLICATION = 'config.wsgi.application'

# ---------------------------------------------------------
# BASE DE DATOS
# ---------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------------------------------
# AUTENTICACIÓN
# ---------------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',   # Permite acceso al frontend
    ],
}

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = ["*"]
CORS_ALLOW_METHODS = ["*"]

# ---------------------------------------------------------
# REGIÓN / IDIOMAS
# ---------------------------------------------------------

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'

USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------
# ESTÁTICOS
# ---------------------------------------------------------

STATIC_URL = 'static/'

# ---------------------------------------------------------
# DEFAULT
# ---------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
