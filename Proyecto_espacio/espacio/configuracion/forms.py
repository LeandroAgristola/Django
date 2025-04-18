from django import forms
from .models import Configuracion

class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = Configuracion
        fields = '__all__'
        widgets = {
            'horario_semana': forms.TextInput(attrs={'placeholder': 'Lunes a Viernes de 8 a 21 hs.'}),
            'horario_sabado': forms.TextInput(attrs={'placeholder': 'Sábados de 9 a 13 hs.'}),
        }