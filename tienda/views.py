from django.shortcuts import render
from .models import Cliente
# Create your views here.


# Create your views here.
def vista_cliente(request):
    listado_clientes= Cliente.objects.all()
    return render(request, 'cliente/vista_cliente.html', {'clientes_mostrar': listado_clientes})
 