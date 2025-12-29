def registrar_auditoria(
    usuario,
    accion,
    modelo,
    objeto_id=None,
    descripcion="",
    ip=None
):
    from .models import Auditoria

    Auditoria.objects.create(
        usuario=usuario,
        accion=accion,
        modelo=modelo,
        objeto_id=objeto_id,
        descripcion=descripcion,
        ip=ip
    )
