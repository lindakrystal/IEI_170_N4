from django.db import models
from django.core.exceptions import ValidationError
from django.db import transaction

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    stock = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def clean(self):
        if self.stock < 0:
            raise ValidationError("El stock no puede ser negativo.")
        if self.stock_minimo < 0:
            raise ValidationError("El stock mínimo no puede ser negativo.")

    def __str__(self):
        return f"{self.sku} - {self.nombre}"


class MovimientoStock(models.Model):
    ENTRADA = 'IN'
    SALIDA = 'OUT'

    TIPOS = [
        (ENTRADA, 'Entrada'),
        (SALIDA, 'Salida'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="movimientos")
    tipo = models.CharField(max_length=3, choices=TIPOS)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    nota = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Movimiento de Stock"
        verbose_name_plural = "Movimientos de Stock"

    def clean(self):
        if self.tipo == self.SALIDA and self.producto.stock - self.cantidad < 0:
            raise ValidationError("Este movimiento dejaría el stock negativo.")

    def save(self, *args, **kwargs):
        self.full_clean()
        with transaction.atomic():
            producto = Producto.objects.select_for_update().get(pk=self.producto_id)
            if self.tipo == self.ENTRADA:
                producto.stock += self.cantidad
            else:
                producto.stock -= self.cantidad

            if producto.stock < 0:
                raise ValidationError("El stock no puede quedar negativo.")

            producto.save()
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_tipo_display()} {self.cantidad} de {self.producto}"
