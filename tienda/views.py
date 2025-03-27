from django.shortcuts import render, redirect
from .models import *
from datetime import datetime
from .forms import RegistroForm
from django.contrib.auth.models import Group



# Create your views here.


# Create your views here.
def vista_cliente(request):
    listado_clientes= Cliente.objects.all()
    return render(request, 'cliente/vista_cliente.html', {'clientes_mostrar': listado_clientes})


def index(request):
    if("fecha_inicio" not in request.session):
        request.session["fecha_inicio"] = datetime.now().strftime('%d/%m/%Y %H:%M')

    return render(request, 'index.html')

def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            if rol == Usuario.CLIENTE:
                grupo = Group.objects.get(name='Clientes')
                grupo.user_set.add(user)
                cliente = Cliente.objects.create(usuario=user)
                cliente.save()
            return redirect('inicio')
    else:
        formulario = RegistroForm()

    return render(request, 'registration/signup.html', {'formulario': formulario})

