from django import forms
from django.core.exceptions import ValidationError
from .models import Evento
from django.utils import timezone
from datetime import datetime
import re
from clientes.models import Cliente
from eventos.models import InscripcionEvento
from django.forms import DateInput

# Validaciones generales
def validar_solo_letras(valor):
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', valor):
        raise ValidationError('Este campo solo debe contener letras y espacios.')

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
            'fecha': DateInput(format='%Y-%m-%d', attrs={'class': 'form-control','type': 'date'}),
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
        
        if self.instance and self.instance.pk:
            self.fields['fecha'].initial = self.instance.fecha.strftime('%Y-%m-%d')
            self.fields['hora'].initial = self.instance.hora.strftime('%H:%M')
            
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

        if precio and precio > 0:
            if not metodo:
                raise ValidationError("Seleccioná al menos un método de pago.")
            if metodo == 'enlace' and not link_pago:
                self.add_error('link_pago', 'Debés ingresar el enlace de pago.')
            if metodo == 'estudio':
                cleaned_data['pago_en_estudio'] = True
                cleaned_data['pago_enlace'] = ''
                cleaned_data['link_pago'] = ''
            elif metodo == 'enlace':
                cleaned_data['pago_en_estudio'] = False
                cleaned_data['pago_enlace'] = link_pago.strip() if link_pago else ''
        else:
            cleaned_data['pago_en_estudio'] = False
            cleaned_data['pago_enlace'] = ''
            cleaned_data['link_pago'] = ''
            cleaned_data['metodo_pago'] = ''

        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if fecha and hora:
            new_datetime = timezone.make_aware(datetime.combine(fecha, hora))
            now = timezone.now()
            
            # solo validar en creación
            if not self.instance.pk and new_datetime < now:
                self.add_error('fecha', "La fecha y hora deben ser posteriores a la actual.")
                self.add_error('hora', "La fecha y hora deben ser posteriores a la actual.")
                raise ValidationError("La fecha y hora no pueden ser en el pasado.")

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
    

TIPO_CLIENTE_CHOICES = (
    ('cargado', 'Cliente cargado'),
    ('nuevo', 'Nuevo cliente'),
)


class InscribirClienteForm(forms.Form):
    tipo_cliente = forms.ChoiceField(
        choices=TIPO_CLIENTE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_tipo_cliente'})
    )

    # Comunes
    estado = forms.ChoiceField(
        choices=InscripcionEvento.ESTADOS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Solo para nuevo cliente
    nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    apellido = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    telefono = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        tipo_cliente = self.cleaned_data.get('tipo_cliente')
        
        if tipo_cliente == 'nuevo':
            if Cliente.objects.filter(mail=email).exists():
                raise ValidationError("Este correo electrónico ya está registrado.")
        return email