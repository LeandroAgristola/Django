from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import Evento
import re

# Validación: solo letras
def validar_solo_letras(valor):
    if not valor.isalpha():
        raise ValidationError('Este campo debe contener solo letras.')

# Validación: solo números
def validar_solo_numeros(valor):
    if not re.match(r'^\d+$', valor):
        raise ValidationError('El número de teléfono debe contener solo números.')

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            'titulo', 'descripcion', 'fecha', 'hora', 'imagen', 'ubicacion', 'cupos',
            'precio', 'mostrar_en_web'
        ]

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ubicación'}),
            'cupos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cupos'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'mostrar_en_web': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
      
        }

    def clean_titulo(self):
        return self._validar_letras('titulo')

    def clean_descripcion(self):
        return self._validar_letras('descripcion')

    def clean_mostrar_en_web(self):
        mostrar_en_web = self.cleaned_data.get('mostrar_en_web')
        return mostrar_en_web

    def _validar_letras(self, campo):
        valor = self.cleaned_data.get(campo)
        validar_solo_letras(valor)
        return valor
