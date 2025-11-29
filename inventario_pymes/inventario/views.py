from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Categoria, Proveedor, Producto, MovimientoStock
from .serializers import (
    CategoriaSerializer,
    ProveedorSerializer,
    ProductoSerializer,
    MovimientoStockSerializer
)


# ----------------------------
# CATEGORÍA
# ----------------------------

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre"]
    ordering_fields = ["nombre"]


# ----------------------------
# PROVEEDOR
# ----------------------------

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre", "correo"]
    ordering_fields = ["nombre"]


# ----------------------------
# PRODUCTO (PRO)
# ----------------------------

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # FILTROS POR CATEGORÍA, PROVEEDOR Y STOCK
    filterset_fields = {
        "categoria": ["exact"],
        "proveedor": ["exact"],
        "stock": ["gte", "lte"],   # mayor o menor stock
    }

    # BÚSQUEDAS
    search_fields = ["nombre", "sku"]

    # ORDENAMIENTO
    ordering_fields = ["nombre", "sku", "stock", "precio"]


# ----------------------------
# MOVIMIENTO DE STOCK (PRO)
# ----------------------------

class MovimientoStockViewSet(viewsets.ModelViewSet):
    queryset = MovimientoStock.objects.all()
    serializer_class = MovimientoStockSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = {
        "producto": ["exact"],
        "tipo": ["exact"],      # Entrada o salida
        "fecha": ["gte", "lte"],  # rango de fechas
    }

    search_fields = ["nota", "producto__nombre"]
    ordering_fields = ["fecha", "cantidad"]
