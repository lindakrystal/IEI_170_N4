"""
Django settings for config project.
Configuración final con DRF, filtros, swagger y permisos PRO.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------
# SECURITY
# ---------------------------------------------------------

SECRET_KEY = 'django-insecure--c7pmeu1fk79x-t*1e0k_^7_b$(@s66o@bdn*853a@4g4teg+-'
DEBUG = True
ALLOWED_HOSTS = []

# ---------------------------------------------------------
# APLICACIONES INSTALADAS
# ---------------------------------------------------------

INSTALLED_APPS = [
    # Base Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django REST Framework
    'rest_framework',
    'rest_framework.authtoken',

    # Filtros y ordenamiento
    'django_filters',

    # Documentación Swagger
    'drf_yasg',

    # CORS para frontend externo
    'corsheaders',

    # App del proyecto
    'inventario',
]

# ---------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # CORS debe ir arriba
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ---------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------------------------------
# VALIDACIÓN DE CONTRASEÑAS
# ---------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------
# INTERNACIONALIZACIÓN
# ---------------------------------------------------------

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'

USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------
# ARCHIVOS ESTÁTICOS
# ---------------------------------------------------------

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------
# CONFIGURACIÓN REST FRAMEWORK (PRO)
# ---------------------------------------------------------

REST_FRAMEWORK = {
    # Autenticación por Token
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    # Permisos globales: autenticación requerida
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    # Filtros, búsqueda y ordenamiento global
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

    # Paginación global
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# ---------------------------------------------------------
# CONFIGURACIÓN CORS
# ---------------------------------------------------------

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",   # React u otro frontend
]

CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]
CORS_ALLOW_CREDENTIALS = True
