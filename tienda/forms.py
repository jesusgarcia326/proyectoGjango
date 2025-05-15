from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django.forms import ModelForm
from .models import *
import datetime

class RegistroForm(UserCreationForm):
    roles = (
        (Usuario.CLIENTE, 'cliente'),
        (Usuario.VENDEDOR, 'vendedor'),
    )

    rol = forms.ChoiceField(choices=roles)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'rol')


class EntradaModelForm(ModelForm):
    class Meta:
        model = Entrada 
        fields = ['nombre', 'fecha']
        labels = {
            "nombre":("Nombre de la fiesta"),
            "fecha":("Fecha de la fiesta"),
        }
        help_texts = {
            "nombre":("Nombre corto y decriptivo"),
            "fecha":("Dia y horade la fiesta"),
        }
        widgets = {
            'fecha': forms.DateInput(format="%Y-%m-%d" ,attrs={'type': 'date', 'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()

        nombre = cleaned_data.get('nombre')
        fecha = cleaned_data.get('fecha')

        if nombre and len(nombre) < 5:
            self.add_error('nombre', 'Escribe un nombre más grande, pisha')

        if fecha and fecha.date() < datetime.date.today():
            self.add_error('fecha', 'La fecha no puede estar en el pasado, pisha')


        return cleaned_data
    


class DiscotecaModelForm(ModelForm):
    class Meta:
        model = Discoteca 
        fields = ['nombre', 'direccion', 'aforo']
        labels = {
            "nombre":("Nombre de la discoteca"),
            "direccion":("Direccion de la discoteca"),
            "aforo":("Aforo de la discoteca")
            
        }
        help_texts = {
            "nombre":("Nombre corto y decriptivo"),
            "direccion":("Direccion de la discoteca"),
            "aforo":("Personas que caben en la discoteca")
        }        
        widgets = {
            'aforo': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
        }       

    def clean(self):
        cleaned_data = super().clean()

        nombre = cleaned_data.get('nombre')
        direccion = cleaned_data.get('direccion')
        aforo = cleaned_data.get('aforo')

        if nombre and len(nombre) > 30:
            self.add_error('nombre', 'Que es una duiscoteca o un libro de historia? pisha')

        if aforo is not None and aforo < 50:
            self.add_error('aforo', 'pa tener ese aforo crea un bar, pisha')

        return cleaned_data


class BancoModelForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = ['banco', 'IBAN', 'moneda']
        labels = {
            'banco': 'Entidad bancaria',
            'IBAN': 'Número IBAN',
            'moneda': 'Tipo de moneda',
        }
        widgets = {
            'banco': forms.TextInput(attrs={'class': 'form-control'}),
            'IBAN': forms.TextInput(attrs={'class': 'form-control'}),
            'moneda': forms.Select(attrs={'class': 'form-control'}),
        }


class DatosVendedorModelForm(ModelForm):
    class Meta:
        model = DatosVendedor
        fields = ['direccion', 'facturacion']
        labels = {
            'direccion': 'Dirección',
            'facturacion': 'Facturación'
        }
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'facturacion': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        

class InventarioModelForm(ModelForm):
    class Meta:
        model = Inventario
        fields = ['discoteca', 'entrada', 'stock','precio']
        labels = {
            'discoteca': 'Discoteca',
            'entrada': 'Entrada',
            'stock': 'Stock',
            "precio":("Precio de la entrada")
        }
        widgets = {
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'entrada': forms.Select(attrs={'class': 'form-control'}),
            # 'discoteca' lo sobrescribimos en __init__
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        if self.request and hasattr(self.request.user, 'vendedor'):
            discotecasdisponibles = Discoteca.objects.filter(vendedor=self.request.user.vendedor)
        else:
            discotecasdisponibles = Discoteca.objects.none()

        self.fields['discoteca'] = forms.ModelChoiceField(
            queryset=discotecasdisponibles,
            widget=forms.Select(attrs={'class': 'form-control'}),
            required=True,
            empty_label="Ninguna"
        )

class BusquedaInventario(forms.Form):
    nombre = forms.CharField(label="Nombre de la entrada", required=False)


class CrearPedidoForms(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['inventario', 'cantidad', 'direccion']
        help_texts = {
            'inventario': "Elija la entrada que desea",
        }
        widgets = {
            'fecha_pedido': forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
        }


class PedidoModelForm(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields = ['cantidad', 'direccion']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        self.inventario= kwargs.pop("inventario")
        super(PedidoModelForm,self).__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super().clean()

        cantidad = cleaned_data.get('cantidad')
        
        if cantidad > self.inventario.stock:
            self.add_error('cantidad', 'te has cola')
        

        return cleaned_data