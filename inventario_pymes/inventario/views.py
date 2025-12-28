from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Categoria, Proveedor, Producto, MovimientoStock
from .serializers import (
    CategoriaSerializer,
    ProveedorSerializer,
    ProductoSerializer,
    MovimientoStockSerializer
)

# ============================================
#   CATEGORÍA
# ============================================

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre"]
    ordering_fields = ["nombre"]


# ============================================
#   PROVEEDOR
# ============================================

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre", "correo"]
    ordering_fields = ["nombre"]


# ============================================
#   PRODUCTO
# ============================================

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = {
        "categoria": ["exact"],
        "proveedor": ["exact"],
        "stock": ["gte", "lte"],
    }

    search_fields = ["nombre", "sku"]
    ordering_fields = ["nombre", "sku", "stock", "precio"]


# ============================================
#   MOVIMIENTO DE STOCK
# ============================================

class MovimientoStockViewSet(viewsets.ModelViewSet):
    queryset = MovimientoStock.objects.all()
    serializer_class = MovimientoStockSerializer
    permission_classes = [permissions.AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = {
        "producto": ["exact"],
        "tipo": ["exact"],
        "fecha": ["gte", "lte"],
    }

    search_fields = ["nota", "producto__nombre"]
    ordering_fields = ["fecha", "cantidad"]


# ============================================
#   LOGIN PARA REACT
# ============================================

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Credenciales inválidas"}, status=400)

    token, created = Token.objects.get_or_create(user=user)

    return Response({"token": token.key})

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Producto, Categoria
from .ai import sugerencia_reposicion, detectar_anomalias_salida, sugerir_categoria_por_texto

@api_view(["GET"])
@permission_classes([AllowAny])
def ai_reposicion(request):
    dias_hist = int(request.query_params.get("dias_hist", 30))
    cubrir = int(request.query_params.get("cubrir", 14))

    data = [sugerencia_reposicion(p, dias_hist=dias_hist, cubrir_dias=cubrir)
            for p in Producto.objects.all().order_by("id")]
    return Response(data)

@api_view(["GET"])
@permission_classes([AllowAny])
def ai_anomalias(request):
    dias = int(request.query_params.get("dias", 30))
    factor = float(request.query_params.get("factor", 3.0))

    out = []
    for p in Producto.objects.all():
        out.extend(detectar_anomalias_salida(p, dias=dias, factor=factor))
    return Response(out)

@api_view(["POST"])
@permission_classes([AllowAny])
def ai_sugerir_categoria(request):
    nombre = request.data.get("nombre", "")
    descripcion = request.data.get("descripcion", "")

    sugerida = sugerir_categoria_por_texto(nombre, descripcion)
    if not sugerida:
        return Response({"categoria_sugerida": None})

    # opcional: si existe en BD, también devuelve su ID
    cat = Categoria.objects.filter(nombre__iexact=sugerida).first()
    return Response({
        "categoria_sugerida": sugerida,
        "categoria_id": cat.id if cat else None
    })
