from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import Empleado
import re

# Validación: solo letras
def validar_solo_letras(valor):
    if not valor.isalpha():
        raise ValidationError('Este campo debe contener solo letras.')

# Validación: solo números
def validar_solo_numeros(valor):
    if not re.match(r'^\d+$', valor):
        raise ValidationError('El número de teléfono debe contener solo números.')

# Validación: email válido
def validar_email(valor):
    try:
        EmailValidator()(valor)
    except ValidationError:
        raise ValidationError('Por favor, ingresa un correo válido.')

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            'nombre', 'apellido', 'email', 'direccion', 'telefono',
            'instagram', 'fecha_alta', 'imagen_perfil', 'mostrar_en_web'
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@usuario'}),
            'fecha_alta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'imagen_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'mostrar_en_web': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_nombre(self):
        return self._validar_letras('nombre')

    def clean_apellido(self):
        return self._validar_letras('apellido')

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        validar_solo_numeros(telefono)
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validar_email(email)
        return email

    def clean_mostrar_en_web(self):
        mostrar_en_web = self.cleaned_data.get('mostrar_en_web')
        if mostrar_en_web and Empleado.objects.filter(mostrar_en_web=True).count() >= 4:
            raise forms.ValidationError("Solo se pueden mostrar 4 empleados en la web pública.")
        return mostrar_en_web

    def _validar_letras(self, campo):
        valor = self.cleaned_data.get(campo)
        validar_solo_letras(valor)
        return valor
