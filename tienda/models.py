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
    
    def __str__(self):
        return self.nombre

class Discoteca(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    aforo = models.IntegerField()
    
    vendedor = models.ForeignKey(Vendedor,on_delete= models.CASCADE,default=None,null=True)
    entrada = models.ManyToManyField(Entrada, through='Inventario')
    
    def __str__(self):
        return self.nombre
    
   
class Banco(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete = models.CASCADE)
    banco= models.CharField(max_length=100)
    IBAN= models.CharField(max_length=100)
    MONEDAS = [
        ("EU","Euro"),
        ("DOL","Dolar"),
        ("LIB","Libra"),
    ]
    moneda = models.CharField(
        max_length=3,
        choices=MONEDAS,
        default="EU"
    )

class DatosVendedor(models.Model):
    vendedor = models.OneToOneField(Vendedor, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    facturacion = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  
    
    
    
class Inventario(models.Model):
    discoteca = models.ForeignKey(Discoteca, on_delete=models.CASCADE)
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)