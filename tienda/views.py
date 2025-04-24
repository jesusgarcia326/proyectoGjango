from django.shortcuts import render, redirect
from .models import *
from datetime import datetime
from .forms import RegistroForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from .forms import *
from django.contrib import messages #esto para los mensajes cuando eduitas o haces algo 
from django.contrib.auth import login
from django.http import Http404




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

def eliminar_entrada (request,entrada_id):
    entrada = Entrada.objects.get(id=entrada_id)
    try:
        entrada.delete()
        messages.success(request,"Se ha eliminado la entrada")

    except Exception as capturo_error:
        print(capturo_error)
    return redirect('vista_entrada')

def vista_discoteca(request):
    listado_discotecas = Discoteca.objects.filter(vendedor=request.user.vendedor).all()
    return render(request, 'discoteca/vista_discoteca.html', {'discotecas_mostrar': listado_discotecas})

def crear_discoteca(request):
    if request.method == 'POST':
        form = DiscotecaModelForm(request.POST)
        if form.is_valid():
            Discoteca.objects.create(
                nombre = form.cleaned_data.get("nombre"),
                direccion = form.cleaned_data.get("direccion"),
                aforo = form.cleaned_data.get("aforo"),
                vendedor = request.user.vendedor
)
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
            user = formulario.save()  # Guarda directamente el usuario
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

            login(request, user)  # Inicia sesión directamente
            return redirect('inicio')
    else:
        formulario = RegistroForm()

    return render(request, 'registration/signup.html', {'formulario': formulario})



def perfil_cliente(request, id_cliente):
    if request.user.cliente.id == id_cliente:
        cliente = Cliente.objects.get(id=id_cliente)
        banco = Banco.objects.filter(cliente=cliente).first()
        return render(request, 'perfil/perfil_cliente.html', {
            'cliente': cliente,
            'banco': banco
        })
    else:
        raise Http404()

def perfil_vendedor(request, id_vendedor):
    try:
        if request.user.vendedor.id == id_vendedor:
            vendedor = Vendedor.objects.get(id=id_vendedor)
            datos = DatosVendedor.objects.filter(vendedor=vendedor).first()

            return render(request, 'perfil/perfil_vendedor.html', {
                'datos': datos,
                'vendedor': vendedor
            })
        else:
            raise Http404()
    except Vendedor.DoesNotExist:
        raise Http404()


def crear_banco(request):
    if request.method == 'POST':
        form = BancoModelForm(request.POST)
        if form.is_valid():
            try:
                banco = Banco.objects.create(
                    banco=form.cleaned_data.get('banco'),
                    IBAN=form.cleaned_data.get('IBAN'),
                    moneda=form.cleaned_data.get('moneda'),
                    cliente=request.user.cliente
                )
                banco.save()
                messages.success(request, "Cuenta bancaria creada correctamente")
                return redirect('perfil_cliente',id_cliente=request.user.cliente.id)
            except Exception as error:
                print(error)
                messages.error(request, "Ha ocurrido un error al crear la cuenta bancaria")
    else:
        form = BancoModelForm()

    return render(request, 'banco/crear_banco.html', {'form': form})


def editar_banco(request, banco_id):
    banco = Banco.objects.get(id=banco_id)
    if request.method == 'POST':
        form = BancoModelForm(request.POST, instance=banco)
        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta bancaria actualizada correctamente")
            return redirect('perfil_cliente',id_cliente=request.user.cliente.id)
    else:
        form = BancoModelForm(instance=banco)
    return render(request, 'banco/editar_banco.html', {'form': form})



def eliminar_banco(request, banco_id):
    banco = Banco.objects.get(id=banco_id)
    cliente_id = banco.cliente.id
    banco.delete()
    messages.success(request, "Cuenta bancaria eliminada correctamente")
    return redirect('perfil_cliente',id_cliente=request.user.cliente.id)


def crear_datos_vendedor(request):
    if request.method == 'POST':
        form = DatosVendedorModelForm(request.POST)
        if form.is_valid():
            try:
                datos = DatosVendedor.objects.create(
                    direccion=form.cleaned_data.get('direccion'),
                    facturacion=form.cleaned_data.get('facturacion'),
                    vendedor=request.user.vendedor  # Asegúrate que el usuario tiene un vendedor asociado
                )
                datos.save()
                messages.success(request, "Datos del vendedor creados correctamente")
                return redirect('perfil_vendedor',id_vendedor=request.user.vendedor.id)
            except Exception as error:
                print(error)
                messages.error(request, "Ha ocurrido un error al guardar los datos del vendedor")
    else:
        form = DatosVendedorModelForm()

    return render(request, 'datos_vendedor/crear.html', {'form': form})

def vista_datos_vendedor(request):
    datos = DatosVendedor.objects.all()
    return render(request, 'datos_vendedor/vista.html', {'datos_vendedor': datos})


def editar_datos_vendedor(request, datos_id):
    datos = DatosVendedor.objects.get(id=datos_id)
    if request.method == 'POST':
        form = DatosVendedorModelForm(request.POST, instance=datos)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos actualizados correctamente")
            return redirect('perfil_vendedor',id_vendedor=request.user.vendedor.id)
    else:
        form = DatosVendedorModelForm(instance=datos)
    return render(request, 'datos_vendedor/editar.html', {'form': form})


def eliminar_datos_vendedor(request, datos_id):
    datos = DatosVendedor.objects.get(id=datos_id)
    datos.delete()
    messages.success(request, "Datos eliminados correctamente")
    return redirect('perfil_vendedor',id_vendedor=request.user.vendedor.id)



def crear_inventario(request):
    if request.method == 'POST':
        form = InventarioModelForm(request.POST,request=request)
        if form.is_valid():
            try:
                datos = Inventario.objects.create(
                    discoteca=form.cleaned_data.get('discoteca'),
                    entrada=form.cleaned_data.get('entrada'),
                    stock=form.cleaned_data.get('stock'),
                )
                inventario = Inventario.objects.filter(discoteca = form.cleaned_data.self, entrada = form.cleaned_data.self)
                
                if(inventario in None):
                    datos.save()
                else:
                    inventario.stock+= form.cleaned_data.self("stock")
                    inventarion.save()
                
                messages.success(request, "Se a añadoto a la tienda el produucto")
                return redirect('perfil_vendedor')
            except Exception as error:
                print(error)
                messages.error(request, "Ha ocurrido un error ")
    else:
        form = InventarioModelForm(None,request=request)

    return render(request, 'inventario/crear_inventario.html', {'form': form})

#ERORES
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)
def mi_error_500(request, exception=None):
    return render (request, 'errores/500.html',None, None,500)