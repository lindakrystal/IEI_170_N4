from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Categoria, Proveedor, Producto, MovimientoStock
from .serializers import (
    CategoriaSerializer,
    ProveedorSerializer,
    ProductoSerializer,
    MovimientoStockSerializer
)

# ==============================
#   CATEGORÍAS
# ==============================
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]   # 👈 DESBLOQUEADO


# ==============================
#   PROVEEDORES
# ==============================
class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.AllowAny]   # 👈 DESBLOQUEADO


# ==============================
#   PRODUCTOS
# ==============================
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.select_related('categoria', 'proveedor').all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.AllowAny]   # 👈 DESBLOQUEADO
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'proveedor', 'stock']
    search_fields = ['nombre', 'sku']
    ordering_fields = ['nombre', 'sku', 'stock']


# ==============================
#   MOVIMIENTOS DE STOCK
# ==============================
class MovimientoStockViewSet(viewsets.ModelViewSet):
    queryset = MovimientoStock.objects.select_related('producto').all()
    serializer_class = MovimientoStockSerializer
    permission_classes = [permissions.AllowAny]   # 👈 DESBLOQUEADO
