from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.telefono

class Cancha(models.Model):
    nombre = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    nombre_cliente = models.CharField(max_length=200)
    telefono_cliente = models.CharField(max_length=20)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    # Las reservas entran automáticamente como confirmadas
    estado = models.CharField(max_length=20, default='CONFIRMADA')

    def __str__(self):
        return f"{self.nombre_cliente} - {self.fecha}"