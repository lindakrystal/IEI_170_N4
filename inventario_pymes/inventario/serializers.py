from rest_framework import serializers
from .models import Categoria, Proveedor, Producto, MovimientoStock
from django.core.exceptions import ValidationError as DjangoValidationError


# ----------------------------
# CATEGORÍA
# ----------------------------

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


# ----------------------------
# PROVEEDOR
# ----------------------------

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


# ----------------------------
# PRODUCTO (CON VALIDACIONES)
# ----------------------------

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    proveedor_nombre = serializers.ReadOnlyField(source='proveedor.nombre')

    class Meta:
        model = Producto
        fields = [
            'id', 'sku', 'nombre', 'descripcion',
            'categoria', 'categoria_nombre',
            'proveedor', 'proveedor_nombre',
            'stock', 'stock_minimo', 'precio'
        ]

    # VALIDACIONES INDIVIDUALES

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock no puede ser negativo.")
        return value

    def validate_stock_minimo(self, value):
        if value < 0:
            raise serializers.ValidationError("El stock mínimo no puede ser negativo.")
        return value

    def validate_precio(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return value


# ----------------------------
# MOVIMIENTO DE STOCK (PRO)
# ----------------------------

class MovimientoStockSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = MovimientoStock
        fields = [
            'id', 'producto', 'producto_nombre',
            'tipo', 'cantidad', 'fecha', 'nota'
        ]

    # Validación previa a guardar
    def validate(self, data):
        producto = data['producto']
        tipo = data['tipo']
        cantidad = data['cantidad']

        if tipo == 'OUT' and producto.stock - cantidad < 0:
            raise serializers.ValidationError(
                f"No se puede retirar {cantidad} unidades. "
                f"Stock disponible: {producto.stock}."
            )
        return data

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0.")
        return value

    
    def create(self, validated_data):
        try:
            return MovimientoStock.objects.create(**validated_data)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)
