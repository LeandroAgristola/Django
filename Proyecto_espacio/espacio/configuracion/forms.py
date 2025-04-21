from django import forms
from .models import Configuracion

class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = Configuracion
        fields = '__all__'
        widgets = {
            'nombre_estudio': forms.TextInput(attrs={
                'placeholder': 'Nombre del estudio',
                'class': 'form-control'
            }),
            'direccion': forms.TextInput(attrs={
                'placeholder': 'Dirección',
                'class': 'form-control'
            }),
            'horario_semana_inicio': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'horario_semana_fin': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'horario_sabado_inicio': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'horario_sabado_fin': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'maps': forms.TextInput(attrs={
                'placeholder': 'https://maps.google.com/...',
                'class': 'form-control'
            }),
            'telefono': forms.TextInput(attrs={
                'placeholder': 'Teléfono',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'estudio@mail.com',
                'class': 'form-control'
            }),
            'instagram': forms.TextInput(attrs={
                'placeholder': 'https://instagram.com/...',
                'class': 'form-control'
            }),
            'facebook': forms.TextInput(attrs={
                'placeholder': 'https://facebook.com/...',
                'class': 'form-control'
            }),
            'youtube': forms.TextInput(attrs={
                'placeholder': 'https://youtube.com/...',
                'class': 'form-control'
            }),
            'whatsapp': forms.TextInput(attrs={
                'placeholder': 'Teléfono de WhatsApp',
                'class': 'form-control'
            }),
            'texto_hero': forms.Textarea(attrs={
                'placeholder': 'Texto para la sección de héroe',
                'class': 'form-control',
                'rows': 3
            }),
            'cuit': forms.TextInput(attrs={
                'placeholder': 'CUIT',
                'class': 'form-control'
            }),
        }

    def clean(self): # Validacion de horarios
        cleaned_data = super().clean()

        semana_inicio = cleaned_data.get("horario_semana_inicio")
        semana_fin = cleaned_data.get("horario_semana_fin")
        sabado_inicio = cleaned_data.get("horario_sabado_inicio")
        sabado_fin = cleaned_data.get("horario_sabado_fin")

        if semana_inicio and semana_fin:
            if semana_inicio >= semana_fin:
                self.add_error("horario_semana_fin", "El horario de fin debe ser mayor al de inicio.")

        if sabado_inicio and sabado_fin:
            if sabado_inicio >= sabado_fin:
                self.add_error("horario_sabado_fin", "El horario de fin debe ser mayor al de inicio.")