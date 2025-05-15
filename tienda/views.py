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
from django.db import transaction




# Create your views here.


# Create your views here.

@permission_required('tienda.view_cliente')
def vista_cliente(request):
    listado_clientes= Cliente.objects.all()
    return render(request, 'cliente/vista_cliente.html', {'clientes_mostrar': listado_clientes})

@permission_required('tienda.view_vendedor')
def vista_vendedor(request):
    listado_vendedores= Vendedor.objects.all()
    return render(request, 'vendedor/vista_vendedor.html', {'vendedores_mostrar': listado_vendedores})

@permission_required('tienda.view_entrada')
def vista_entradas(request):
    entradas = Entrada.objects.all().order_by('-fecha')
    return render(request, 'entrada/vista_entrada.html', {'entradas_mostrar': entradas})

@permission_required('tienda.add_entrada')
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


@permission_required('tienda.change_entrada')
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


@permission_required('tienda.delete_entrada')
def eliminar_entrada (request,entrada_id):
    entrada = Entrada.objects.get(id=entrada_id)
    try:
        entrada.delete()
        messages.success(request,"Se ha eliminado la entrada")

    except Exception as capturo_error:
        print(capturo_error)
    return redirect('vista_entrada')


@permission_required('tienda.view_discoteca')
def vista_discoteca(request):
    listado_discotecas = Discoteca.objects.filter(vendedor=request.user.vendedor).all()
    return render(request, 'discoteca/vista_discoteca.html', {'discotecas_mostrar': listado_discotecas})


@permission_required('tienda.add_discoteca')
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


@permission_required('tienda.view_discoteca')
def dame_discoteca(request,jaimito):
    discoteca = Discoteca.objects.get(id=jaimito)
    return render(request, 'discoteca/dame_discoteca.html', {'discoteca': discoteca})

@permission_required('tienda.change_discoteca')
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
    if "fecha_inicio" not in request.session:
        request.session["fecha_inicio"] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
        
    vista_producto_cliente = Inventario.objects.all()
    return render(request, 'index.html', {'vista_producto_cliente': vista_producto_cliente})



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


@permission_required('tienda.add_banco')
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


@permission_required('tienda.change_banco')
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


@permission_required('tienda.delete_banco')
def eliminar_banco(request, banco_id):
    banco = Banco.objects.get(id=banco_id)
    cliente_id = banco.cliente.id
    banco.delete()
    messages.success(request, "Cuenta bancaria eliminada correctamente")
    return redirect('perfil_cliente',id_cliente=request.user.cliente.id)


@permission_required('tienda.add_datosvendedor')
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


@permission_required('tienda.change_datosvendedor')
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


@permission_required('tienda.delete_datosvendedor')
def eliminar_datos_vendedor(request, datos_id):
    datos = DatosVendedor.objects.get(id=datos_id)
    datos.delete()
    messages.success(request, "Datos eliminados correctamente")
    return redirect('perfil_vendedor',id_vendedor=request.user.vendedor.id)


@permission_required('tienda.add_inventario')
def crear_inventario(request):
    if request.method == 'POST':
        formulario = InventarioModelForm(request.POST, request=request)
        if formulario.is_valid():
            try:
                discoteca = formulario.cleaned_data.get('discoteca')
                entrada = formulario.cleaned_data.get('entrada')
                stock = formulario.cleaned_data.get('stock')

                inventario = Inventario.objects.filter(discoteca=discoteca, entrada=entrada).first()

                if inventario is None:
                    formulario.save()
                else:
                    inventario.stock += stock
                    inventario.save()

                messages.success(request, "Se ha añadido a la tienda el producto")
                return redirect('perfil_vendedor')
            except Exception as error:
                print(error)
                messages.error(request, "Ha ocurrido un error")
    else:
        formulario = InventarioModelForm(None, request=request)

    return render(request, 'inventario/crear_inventario.html', {'form': formulario})


@permission_required('tienda.view_inventario')
def lista_productos(request, vendedor_id):
    if request.user.vendedor.id != vendedor_id:
        raise Http404("Paguina no encontrada Error 404")

    productos = Inventario.objects.filter(discoteca__vendedor=request.user.vendedor)
    return render(request, 'inventario/lista_productos.html', {'productos': productos})


@permission_required('tienda.view_inventario')
def ver_producto(request, id_producto):
    try:
        producto = Inventario.objects.get(id=id_producto)
    except Inventario.DoesNotExist:
        raise Http404("Producto no encontrado")
    
    return render(request, 'inventario/ver_producto.html', {'producto': producto})


@permission_required('tienda.change_inventario')
def editar_producto(request, id_producto):
    producto = Inventario.objects.get(id=id_producto)

    if request.method == 'POST':
        formulario = InventarioModelForm(request.POST, request=request, instance=producto)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto actualizado correctamente")
            return redirect('lista_productos', vendedor_id=producto.discoteca.vendedor.id)

    else:
        formulario = InventarioModelForm(request=request, instance=producto)
    
    return render(request, 'inventario/editar_producto.html', {'formulario': formulario, 'producto': producto})


@permission_required('tienda.delete_inventario')
def eliminar_producto(request, id_producto):
    producto = Inventario.objects.get(id=id_producto)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente")
    return redirect('lista_productos', vendedor_id=producto.discoteca.vendedor.id)


def buscarProductos(request):
    formulario = BusquedaInventario(request.GET or None)
    productos = Inventario.objects.all()

    if request.GET and formulario.is_valid():
        nombre = formulario.cleaned_data.get("nombre")
        productos = Inventario.objects.filter(entrada__nombre__icontains=nombre)

    return render(request, 'inventario/buscar_productos.html', {
        'productos': productos,
        'formulario': formulario
    })


@permission_required('tienda.add_pedidos')
def crear_pedidos(request):
    if request.method == 'POST':
        formulario = CrearPedidoForms(request.POST)
        if formulario.is_valid():
            pedido = formulario.save(commit=False)
            pedido.fecha_pedido = timezone.now()
            pedido.cliente = request.user.cliente
            pedido.save()
            messages.success(request, 'Se ha creado su pedido correctamente')
            return redirect('inicio')
    else:
        formulario = CrearPedidoForms()

    return render(request, 'cliente/crear_pedidos.html', {'formulario': formulario})


@permission_required('tienda.add_pedidos')
def comprar_producto(request, id_inventario):
    try:
        inventario = Inventario.objects.get(id=id_inventario)
    except Inventario.DoesNotExist:
        raise Http404("El producto no existe")

    if request.method == 'POST':
        form = PedidoModelForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data.get('cantidad')
            direccion = form.cleaned_data.get('direccion')

            if cantidad > inventario.stock:
                messages.error(request, "No hay suficiente stock disponible.")
            else:
                pedido = Pedidos.objects.create(
                    cliente=request.user.cliente,
                    inventario=inventario,
                    cantidad=cantidad,
                    direccion=direccion
                )
                pedido.save()
                inventario.stock -= cantidad
                inventario.save()
                messages.success(request, "¡Pedido realizado con éxito!")
                return redirect('inicio')
    else:
        form = PedidoModelForm()

    return render(request, 'producto/comprar_producto.html', {
        'form': form,
        'inventario': inventario
    })

#ERORES
def mi_error_404(request, exception):
    return render(request, 'errores/404.html', status=404)

def mi_error_500(request):
    return render(request, 'errores/500.html', status=500)