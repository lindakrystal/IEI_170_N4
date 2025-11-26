from django.contrib import admin
from .models import Categoria, Proveedor, Producto, MovimientoStock

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono')
    search_fields = ('nombre', 'correo')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nombre', 'categoria', 'proveedor', 'stock', 'stock_minimo', 'precio')
    list_filter = ('categoria', 'proveedor')
    search_fields = ('sku', 'nombre')

@admin.register(MovimientoStock)
class MovimientoStockAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo', 'cantidad', 'fecha')
    search_fields = ('producto__nombre',)
    list_filter = ('tipo', 'producto__categoria', 'producto__proveedor')
