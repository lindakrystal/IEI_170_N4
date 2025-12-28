from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from .models import Producto, MovimientoStock

def consumo_promedio_diario(producto: Producto, dias: int = 30) -> float:
    """Promedio diario de salida (OUT) en los últimos 'dias'."""
    desde = timezone.now() - timedelta(days=dias)
    total = (MovimientoStock.objects
             .filter(producto=producto, tipo="OUT", fecha__gte=desde)
             .aggregate(total=Sum("cantidad"))["total"]) or 0
    return total / dias if dias > 0 else 0.0

def sugerencia_reposicion(producto: Producto, dias_hist: int = 30, cubrir_dias: int = 14) -> dict:
    """Sugerencia de reposición basada en consumo histórico."""
    cpd = consumo_promedio_diario(producto, dias=dias_hist)
    stock_actual = producto.stock
    if cpd <= 0:
        return {
            "producto_id": producto.id,
            "sku": producto.sku,
            "nombre": producto.nombre,
            "consumo_promedio_diario": 0,
            "dias_para_quiebre": None,
            "reponer_sugerido": 0,
            "motivo": "Sin consumo histórico suficiente (cpd=0)."
        }

    dias_para_quiebre = stock_actual / cpd if cpd > 0 else None
    objetivo = int(round(cpd * cubrir_dias))
    reponer = max(0, objetivo - stock_actual)

    return {
        "producto_id": producto.id,
        "sku": producto.sku,
        "nombre": producto.nombre,
        "consumo_promedio_diario": round(cpd, 2),
        "dias_para_quiebre": round(dias_para_quiebre, 1),
        "reponer_sugerido": reponer,
        "motivo": f"Cubrir {cubrir_dias} días según consumo promedio."
    }
from django.db.models import Avg

def detectar_anomalias_salida(producto: Producto, dias: int = 30, factor: float = 3.0) -> list[dict]:
    """
    Marca como anomalía si una salida es > (promedio * factor).
    """
    desde = timezone.now() - timedelta(days=dias)
    outs = MovimientoStock.objects.filter(producto=producto, tipo="OUT", fecha__gte=desde)

    promedio = outs.aggregate(avg=Avg("cantidad"))["avg"] or 0
    if promedio <= 0:
        return []

    umbral = promedio * factor
    anom = outs.filter(cantidad__gt=umbral).order_by("-fecha")[:20]

    return [{
        "movimiento_id": m.id,
        "producto_id": producto.id,
        "sku": producto.sku,
        "nombre": producto.nombre,
        "cantidad": m.cantidad,
        "fecha": m.fecha,
        "promedio": round(float(promedio), 2),
        "umbral": round(float(umbral), 2),
        "nota": m.nota,
    } for m in anom]
def sugerir_categoria_por_texto(nombre: str, descripcion: str = "") -> str | None:
    text = f"{nombre} {descripcion}".lower()

    reglas = {
        "Periféricos": ["mouse", "teclado", "audifono", "headset", "monitor", "pad", "webcam"],
        "Redes": ["router", "switch", "cable", "ethernet", "wifi", "antena"],
        "Almacenamiento": ["ssd", "hdd", "disco", "pendrive", "memoria"],
        "Componentes": ["ram", "procesador", "cpu", "gpu", "placa", "motherboard", "fuente"],
    }

    for categoria, palabras in reglas.items():
        if any(p in text for p in palabras):
            return categoria
    return None
def sugerencia_reposicion(producto: Producto, dias_hist: int = 30, cubrir_dias: int = 14) -> dict:
    cpd = consumo_promedio_diario(producto, dias=dias_hist)
    stock_actual = producto.stock

    if cpd <= 0:
        return {
            "producto_id": producto.id,
            "sku": producto.sku,
            "nombre": producto.nombre,
            "nivel": "sin_datos",
            "reponer_sugerido": 0,
            "motivo": "Sin consumo histórico suficiente."
        }

    dias_para_quiebre = stock_actual / cpd if cpd > 0 else None
    objetivo = int(round(cpd * cubrir_dias))
    reponer = max(0, objetivo - stock_actual)

    if dias_para_quiebre <= 3:
        nivel = "critico"
    elif dias_para_quiebre <= 7:
        nivel = "atencion"
    else:
        nivel = "ok"

    return {
        "producto_id": producto.id,
        "sku": producto.sku,
        "nombre": producto.nombre,
        "nivel": nivel,
        "dias_para_quiebre": round(dias_para_quiebre, 1),
        "reponer_sugerido": reponer,
        "motivo": f"Cubrir {cubrir_dias} días según consumo promedio."
    }
