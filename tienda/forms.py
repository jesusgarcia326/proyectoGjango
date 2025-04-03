from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django.forms import ModelForm
from .models import *

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
            "precio":("Precio sin decimales y menos que 50 ")
        }
        widgets = {
            'fecha': forms.DateInput(format="%Y-%m-%d" ,attrs={'type': 'date', 'class': 'form-control'}),
        }
    
    def clean(self):
        super().clean()
        
        nombre = self.cleaned_data.get('nombre')
    
        if len(nombre) < 5:
            self.add_error('nombre', 'Escribe un nombre mas grande pisha')
        return self.cleaned_data
        