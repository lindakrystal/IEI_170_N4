from rest_framework import viewsets, filters
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import (
    Categoria,
    Proveedor,
    Producto,
    MovimientoStock
)
from .serializers import (
    CategoriaSerializer,
    ProveedorSerializer,
    ProductoSerializer,
    MovimientoStockSerializer
)

from .ai import (
    sugerencia_reposicion,
    detectar_anomalias_salida,
    sugerir_categoria_por_texto
)

# =====================================================
# UTILIDAD DE AUDITORÍA
# =====================================================

def log_accion(usuario, accion, objeto):
    print(
        f"[AUDITORÍA] Empresa={usuario.empresa} | "
        f"Usuario={usuario.username} | "
        f"Acción={accion} | "
        f"Objeto={objeto}"
    )


# =====================================================
# CATEGORÍA (ADMIN – POR EMPRESA)
# =====================================================

class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre"]
    ordering_fields = ["nombre"]

    def get_queryset(self):
        return Categoria.objects.filter(
            empresa=self.request.user.empresa
        )

    def perform_create(self, serializer):
        instancia = serializer.save(
            empresa=self.request.user.empresa
        )
        log_accion(self.request.user, "CREAR_CATEGORIA", instancia)


# =====================================================
# PROVEEDOR (ADMIN – POR EMPRESA)
# =====================================================

class ProveedorViewSet(viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre", "correo"]
    ordering_fields = ["nombre"]

    def get_queryset(self):
        return Proveedor.objects.filter(
            empresa=self.request.user.empresa
        )

    def perform_create(self, serializer):
        instancia = serializer.save(
            empresa=self.request.user.empresa
        )
        log_accion(self.request.user, "CREAR_PROVEEDOR", instancia)


# =====================================================
# PRODUCTO (ADMIN – POR EMPRESA)
# =====================================================

class ProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

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

    def get_queryset(self):
        return Producto.objects.filter(
            empresa=self.request.user.empresa
        )

    def perform_create(self, serializer):
        instancia = serializer.save(
            empresa=self.request.user.empresa
        )
        log_accion(self.request.user, "CREAR_PRODUCTO", instancia)


# =====================================================
# MOVIMIENTO DE STOCK (USUARIOS DE LA EMPRESA)
# =====================================================

class MovimientoStockViewSet(viewsets.ModelViewSet):
    serializer_class = MovimientoStockSerializer
    permission_classes = [IsAuthenticated]

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

    def get_queryset(self):
        return MovimientoStock.objects.filter(
            empresa=self.request.user.empresa
        )

    def perform_create(self, serializer):
        instancia = serializer.save(
            empresa=self.request.user.empresa
        )
        log_accion(self.request.user, "MOVIMIENTO_STOCK", instancia)


# =====================================================
# LOGIN (PÚBLICO)
# =====================================================

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    user = authenticate(
        username=request.data.get("username"),
        password=request.data.get("password")
    )

    if user is None or not user.is_active:
        return Response(
            {"error": "Credenciales inválidas"},
            status=400
        )

    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        "token": token.key,
        "username": user.username,
        "empresa": user.empresa.nombre,
        "rol": "ADMIN" if user.is_staff else "USUARIO"
    })


# =====================================================
# IA – REPOSICIÓN (ADMIN – POR EMPRESA)
# =====================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def ai_reposicion(request):
    productos = Producto.objects.filter(
        empresa=request.user.empresa
    )

    data = [
        sugerencia_reposicion(p)
        for p in productos.order_by("id")
    ]

    return Response(data)


# =====================================================
# IA – ANOMALÍAS (ADMIN – POR EMPRESA)
# =====================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def ai_anomalias(request):
    productos = Producto.objects.filter(
        empresa=request.user.empresa
    )

    resultados = []
    for p in productos:
        resultados.extend(
            detectar_anomalias_salida(p)
        )

    return Response(resultados)


# =====================================================
# IA – SUGERIR CATEGORÍA
# =====================================================

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def ai_sugerir_categoria(request):
    sugerida = sugerir_categoria_por_texto(
        request.data.get("nombre", ""),
        request.data.get("descripcion", "")
    )

    if not sugerida:
        return Response({"categoria_sugerida": None})

    categoria = Categoria.objects.filter(
        empresa=request.user.empresa,
        nombre__iexact=sugerida
    ).first()

    return Response({
        "categoria_sugerida": sugerida,
        "categoria_id": categoria.id if categoria else None
    })
