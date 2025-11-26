from rest_framework import serializers
from .models import Categoria, Proveedor, Producto, MovimientoStock

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


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


class MovimientoStockSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = MovimientoStock
        fields = [
            'id', 'producto', 'producto_nombre',
            'tipo', 'cantidad', 'fecha', 'nota'
        ]
