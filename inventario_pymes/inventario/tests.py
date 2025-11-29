from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import Categoria, Proveedor, Producto, MovimientoStock


# ---------------------------------------------------------------
# BASE: CREAR USUARIO + TOKEN PARA TESTS DE LA API
# ---------------------------------------------------------------

class BaseTestCase(TestCase):
    def setUp(self):
        # Crear usuario para autenticación
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        # Categoría y proveedor base
        self.categoria = Categoria.objects.create(nombre="Electrónica")
        self.proveedor = Proveedor.objects.create(nombre="Tech Supplier")

        # Producto de prueba
        self.producto = Producto.objects.create(
            sku="ABC123",
            nombre="Mouse Gamer",
            categoria=self.categoria,
            proveedor=self.proveedor,
            stock=10,
            stock_minimo=2,
            precio=19990
        )


# ---------------------------------------------------------------
# TESTS DE MODELO: STOCK NEGATIVO
# ---------------------------------------------------------------

class TestMovimientosModelo(BaseTestCase):
    def test_movimiento_no_deja_stock_negativo(self):
        """Debe impedir retirar más stock del disponible."""
        movimiento = MovimientoStock(
            producto=self.producto,
            tipo="OUT",
            cantidad=50  # mucho mayor al stock: 10
        )

        # Esperamos un ValidationError
        with self.assertRaises(ValidationError):
            movimiento.full_clean()

    def test_movimiento_entrada_incrementa_stock(self):
        """Entrada aumenta stock correctamente."""
        MovimientoStock.objects.create(
            producto=self.producto,
            tipo="IN",
            cantidad=5
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 15)

    def test_movimiento_salida_correcta(self):
        """Salida válida descuenta correctamente."""
        MovimientoStock.objects.create(
            producto=self.producto,
            tipo="OUT",
            cantidad=4
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 6)


# ---------------------------------------------------------------
# TESTS DE API: ENDPOINTS
# ---------------------------------------------------------------

class TestProductoAPI(BaseTestCase):

    def test_listado_productos_autenticado(self):
        """El endpoint de productos responde autenticado."""
        response = self.client.get("/api/productos/")
        self.assertEqual(response.status_code, 200)

    def test_crear_producto_api(self):
        """Crear un producto desde la API funciona."""
        data = {
            "sku": "XYZ999",
            "nombre": "Teclado mecánico",
            "descripcion": "Switch rojo",
            "categoria": self.categoria.id,
            "proveedor": self.proveedor.id,
            "stock": 5,
            "stock_minimo": 1,
            "precio": 39990
        }

        response = self.client.post("/api/productos/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["nombre"], "Teclado mecánico")

    def test_crear_producto_stock_negativo(self):
        """La API debe impedir stock negativo."""
        data = {
            "sku": "BAD001",
            "nombre": "Producto mal",
            "categoria": self.categoria.id,
            "proveedor": self.proveedor.id,
            "stock": -10,
            "stock_minimo": 0,
            "precio": 10000
        }

        response = self.client.post("/api/productos/", data)
        self.assertEqual(response.status_code, 400)


class TestMovimientoStockAPI(BaseTestCase):

    def test_movimiento_api_retirar_mas_del_stock(self):
        """No permite salida que deje stock negativo vía API."""
        data = {
            "producto": self.producto.id,
            "tipo": "OUT",
            "cantidad": 999,  # mucho más del stock
        }

        response = self.client.post("/api/movimientos/", data)
        self.assertEqual(response.status_code, 400)

    def test_movimiento_api_correcto(self):
        """Salida válida funciona bien vía API."""
        data = {
            "producto": self.producto.id,
            "tipo": "OUT",
            "cantidad": 3,
        }

        response = self.client.post("/api/movimientos/", data)
        self.assertEqual(response.status_code, 201)

        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 7)
