from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from inventario.views import (
    CategoriaViewSet,
    ProveedorViewSet,
    ProductoViewSet,
    MovimientoStockViewSet,
    login_view,
    ai_reposicion,
    ai_anomalias,
    ai_sugerir_categoria
)

# Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


# ============================
# ROUTER (CRUD AUTOMÁTICO)
# ============================

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'movimientos', MovimientoStockViewSet)


# ============================
# SWAGGER
# ============================

schema_view = get_schema_view(
    openapi.Info(
        title="API Inventario PYMES",
        default_version='v1',
        description="Sistema de Inventario con IA para PYMES"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# ============================
# URLS
# ============================

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),

    # API REST (CRUD)
    path('api/', include(router.urls)),

    # Login con Token (React)
    path('api/login/', login_view, name='api_login'),

    # ========================
    # IA 🔥
    # ========================
    path('api/ia/reposicion/', ai_reposicion, name='ai_reposicion'),
    path('api/ia/anomalias/', ai_anomalias, name='ai_anomalias'),
    path('api/ia/sugerir-categoria/', ai_sugerir_categoria, name='ai_sugerir_categoria'),

    # Swagger / Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]
