from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Usuario(AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    VENDEDOR = 3

    ROLES = (
        (ADMINISTRADOR, 'administrador'),
        (CLIENTE, 'cliente'),
        (VENDEDOR, 'bibliotecario'),
    )

    rol = models.PositiveSmallIntegerField(choices=ROLES, default=ADMINISTRADOR)
    
    
class Vendedor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    
    
class Cliente(models.Model):
    # nombre = models.CharField(max_length=100)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)




