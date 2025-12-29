from django.db import models
from django.contrib.auth.models import User

class Auditoria(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    accion = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    objeto_id = models.IntegerField(null=True, blank=True)

    descripcion = models.TextField(blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fecha} - {self.usuario} - {self.accion}"
