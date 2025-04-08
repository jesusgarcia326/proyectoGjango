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
        fields = ['nombre', 'fecha', 'precio']
        labels = {
            "nombre":("Nombre de la fiesta"),
            "fecha":("Fecha de la fiesta"),
            "precio":("Precio de la entrada")
        }
        help_texts = {
            "nombre":("Nombre corto y decriptivo"),
            "fecha":("Dia y horade la fiesta"),
            "precio":("Precio sin decimales")
        }
        widgets = {
            'fecha': forms.DateInput(format="%Y-%m-%d" ,attrs={'type': 'date', 'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()

        nombre = cleaned_data.get('nombre')
        fecha = cleaned_data.get('fecha')
        precio = cleaned_data.get('precio')

        if nombre and len(nombre) < 5:
            self.add_error('nombre', 'Escribe un nombre más grande, pisha')

        if fecha and fecha.date() < datetime.date.today():
            self.add_error('fecha', 'La fecha no puede estar en el pasado, pisha')

        if precio is not None and precio > 50:
            self.add_error('precio', 'El precio no puede ser mayor a 50')

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