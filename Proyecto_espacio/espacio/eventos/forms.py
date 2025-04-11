from django import forms
from django.core.exceptions import ValidationError
from .models import Evento, InscripcionEvento
import re
from datetime import datetime

# Validación: solo letras
def validar_solo_letras(valor):
    for char in valor:
        if not (char.isalpha() or char.isspace()):
            raise ValidationError('Este campo debe contener solo letras y espacios.')

# Validación: solo números
def validar_solo_numeros(valor):
    if not re.match(r'^\d+$', valor):
        raise ValidationError('El número de teléfono debe contener solo números.')

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'fecha', 'hora', 'ubicacion', 'cupos', 'imagen', 'precio','pago_enlace', 'pago_en_estudio', 'link_pago', 'mostrar_en_web']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ubicación'}),
            'cupos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cupos'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'pago_enlace': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pago_en_estudio': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'link_pago': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link de pago'}),
            'mostrar_en_web': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if fecha and hora:
            evento_datetime = datetime.combine(fecha, hora)
            if evento_datetime < datetime.now():
                raise forms.ValidationError("La fecha y hora no pueden ser anteriores a la actual.")

        if cleaned_data.get('pago_enlace') and cleaned_data.get('pago_en_estudio'):
            raise forms.ValidationError("Solo una forma de pago puede estar activa.")

        return cleaned_data

    def clean_titulo(self):
        return self._validar_letras('titulo')

    def _validar_letras(self, campo):
        valor = self.cleaned_data.get(campo)
        validar_solo_letras(valor)
        return valor

    def clean_cupos(self):
        cupos = self.cleaned_data.get('cupos')
        if cupos is not None and cupos < 0:
            raise ValidationError('El número de cupos debe ser mayor o igual a cero.')
        return cupos

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = InscripcionEvento
        fields = ['nombre', 'telefono', 'estado', 'cliente_id']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'cliente_id': forms.TextInput(attrs={'class': 'form-control'}),
        }