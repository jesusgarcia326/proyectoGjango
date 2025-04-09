from django.shortcuts import render, redirect
from .models import *
from datetime import datetime
from .forms import RegistroForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from .forms import *
from django.contrib import messages #esto para los mensajes cuando eduitas o haces algo 



# Create your views here.


# Create your views here.
@permission_required('tienda.view_cliente')
def vista_cliente(request):
    listado_clientes= Cliente.objects.all()
    return render(request, 'cliente/vista_cliente.html', {'clientes_mostrar': listado_clientes})

def vista_vendedor(request):
    listado_vendedores= Vendedor.objects.all()
    return render(request, 'vendedor/vista_vendedor.html', {'vendedores_mostrar': listado_vendedores})

def vista_entradas(request):
    entradas = Entrada.objects.all().order_by('-fecha')
    return render(request, 'entrada/vista_entrada.html', {'entradas_mostrar': entradas})


def crear_entrada(request):
    if request.method == 'POST':
        form = EntradaModelForm(request.POST)
        if form.is_valid():
            print("Es valido")
            form.save()
            messages.success(request,"Se ha creado una entrda")
            return redirect('vista_entrada')
    else:
        form = EntradaModelForm()
    return render(request, 'formulario_entrada/formulario_entrada.html', {'form': form})


def dame_entrada(request,pepito):
    entradas = Entrada.objects.get(id=pepito)
    return render(request, 'entrada/dame_entrada.html', {'entrada': entradas})



def editar_entrada (request,pepito):
    entrada = Entrada.objects.get(id=pepito)
    if request.method == 'POST':
        form = EntradaModelForm(request.POST,instance=entrada)
        if form.is_valid():
            try:
                print("Es válido")
                form.save()
                messages.success(request,"Se ha editado una entrda")
                return redirect('dame_entrada', pepito=pepito)
            except Exception as capturo_error:
                print("Error al guardar:", capturo_error)
    else:
        form = EntradaModelForm(instance=entrada)
    return render(request, 'entrada/editar_entrada.html', {'form': form, "entrada": entrada})



def vista_discoteca(request):
    listado_discotecas = Discoteca.objects.all()
    return render(request, 'discoteca/vista_discoteca.html', {'discotecas_mostrar': listado_discotecas})

def crear_discoteca(request):
    if request.method == 'POST':
        form = DiscotecaModelForm(request.POST)
        if form.is_valid():
            print("Es valido")
            form.save()
            messages.success(request,"Se ha creado una discoteca")
            return render(request, 'discoteca/vista_discoteca.html')

    else:
        form = DiscotecaModelForm()
    return render(request, 'formulario_discoteca/formulario_discoteca.html', {'form': form})

def dame_discoteca(request,jaimito):
    discoteca = Discoteca.objects.get(id=jaimito)
    return render(request, 'discoteca/dame_discoteca.html', {'discoteca': discoteca})

def editar_discoteca (request,jaimito):
    discoteca = Discoteca.objects.get(id=jaimito)
    if request.method == 'POST':
        form = DiscotecaModelForm(request.POST,instance=discoteca)
        if form.is_valid():
            try:
                print("Es válido")
                form.save()
                messages.success(request,"Se ha editado la discoteca")
                return redirect('dame_discoteca', jaimito=jaimito)
            except Exception as capturo_error:
                print("Error al guardar:", capturo_error)
    else:
        form = DiscotecaModelForm(instance=discoteca)
    return render(request, 'discoteca/editar_discoteca.html', {'form': form, "discoteca": discoteca})


def index(request):
    if("fecha_inicio" not in request.session):
        request.session["fecha_inicio"] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    return render(request, 'index.html')

def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save(commit=False)
            user.set_password(formulario.cleaned_data['password1'])  # Porque usas UserCreationForm
            user.save()

            rol = int(formulario.cleaned_data.get('rol'))

            if rol == Usuario.CLIENTE:
                grupo = Group.objects.get(name='Clientes')
                grupo.user_set.add(user)
                cliente = Cliente.objects.create(usuario=user)
                cliente.save()

            elif rol == Usuario.VENDEDOR:
                grupo = Group.objects.get(name='Vendedores')
                grupo.user_set.add(user)
                vendedor = Vendedor.objects.create(usuario=user)
                vendedor.save()

            return redirect('inicio')
    else:
        formulario = RegistroForm()

    return render(request, 'registration/signup.html', {'formulario': formulario})
