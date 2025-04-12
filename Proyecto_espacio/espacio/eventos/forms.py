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

METODO_PAGO_CHOICES = (
    ('', 'Seleccione método de pago'),
    ('estudio', 'Pago en el estudio'),
    ('enlace', 'Pago con enlace'),
)

class EventoForm(forms.ModelForm):
    metodo_pago = forms.ChoiceField(
        choices=METODO_PAGO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_metodo_pago'})
    )

    class Meta:
        model = Evento
        fields = ['titulo', 'mostrar_en_web', 'descripcion', 'fecha', 'hora', 'ubicacion', 'cupos', 'imagen', 'precio',
                  'metodo_pago', 'pago_enlace', 'pago_en_estudio', 'link_pago']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'mostrar_en_web': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ubicación'}),
            'cupos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cupos'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio', 'id': 'id_precio'}),
            # Ocultamos los campos reales de método de pago
            'pago_enlace': forms.HiddenInput(attrs={'class': 'form-check-input', 'style': 'display:none;'}),
            'pago_en_estudio': forms.HiddenInput(attrs={'class': 'form-check-input', 'style': 'display:none;'}),
            # Quitar el style inline para "link_pago"
            'link_pago': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link de pago', 'id': 'id_link_pago'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventoForm, self).__init__(*args, **kwargs)
        # Si estamos en edición, pre-cargamos el método de pago
        if self.instance and self.instance.pk:
            if self.instance.pago_en_estudio:
                self.fields['metodo_pago'].initial = 'estudio'
            elif self.instance.pago_enlace:
                self.fields['metodo_pago'].initial = 'enlace'
            else:
                self.fields['metodo_pago'].initial = ''

    def clean(self):
        cleaned_data = super().clean()
        precio = cleaned_data.get('precio')
        metodo = cleaned_data.get('metodo_pago')
        link_pago = cleaned_data.get('link_pago')

        # Si el precio es mayor a 0, se debe seleccionar un método
        if precio and precio > 0:
            if not metodo:
                raise ValidationError("Seleccioná al menos un método de pago.")
            if metodo == 'enlace' and not link_pago:
                self.add_error('link_pago', 'Debés ingresar el enlace de pago.')
            # Asignamos los valores a los campos reales según la opción elegida:
            if metodo == 'estudio':
                cleaned_data['pago_en_estudio'] = True
                cleaned_data['pago_enlace'] = ''  # Limpiamos el campo de enlace
                cleaned_data['link_pago'] = ''
            elif metodo == 'enlace':
                cleaned_data['pago_en_estudio'] = False
                # En vez de asignar True, asignamos el link proporcionado
                cleaned_data['pago_enlace'] = link_pago.strip() if link_pago else ''
                # Opcional: podrías dejar link_pago o limpiar ese campo, según cómo quieras almacenar el dato
        else:
            # Si el precio es 0 o no se define, se desactivan las opciones de pago
            cleaned_data['pago_en_estudio'] = False
            cleaned_data['pago_enlace'] = ''
            cleaned_data['link_pago'] = ''
            cleaned_data['metodo_pago'] = ''
        return cleaned_data

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