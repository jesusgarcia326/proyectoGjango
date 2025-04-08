from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    VENDEDOR = 3

    ROLES = (
        (ADMINISTRADOR, 'administrador'),
        (CLIENTE, 'cliente'),
        (VENDEDOR, 'vendedor'),
    )

    rol = models.PositiveSmallIntegerField(choices=ROLES, default=ADMINISTRADOR)
    
    
class Vendedor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    
    
class Cliente(models.Model):
    # nombre = models.CharField(max_length=100)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

class Entrada(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateTimeField(default=timezone.now)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

class Discoteca(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    aforo = models.IntegerField()
   


