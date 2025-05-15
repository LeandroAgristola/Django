from django import forms
from .models import Cliente, Plan
from django.core.exceptions import ValidationError
from django.utils import timezone

class ClienteForm(forms.ModelForm):
    dias = forms.CharField(widget=forms.HiddenInput(), required=False)
    horas = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Cliente
        fields =  ['nombre', 'apellido', 'dni', 'telefono', 'mail', 'plan', 'fecha_alta', 'estado']
        exclude = ['activo', 'modificado']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'dni': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'DNI'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'plan': forms.Select(attrs={'class': 'form-control'}),
            'fecha_alta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','format': 'yyyy-MM-dd'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.dias_lista = []
        self.horas_lista = []
        super().__init__(*args, **kwargs)

        # Capturar los turnos si vienen por POST
        data = args[0] if args else None
        if data:
            self.dias_lista = data.getlist('dias[]')
            self.horas_lista = data.getlist('horas[]')

            # Asignarlos al cliente para que pasen el clean() del modelo
            dias_str = ", ".join(self.dias_lista)
            horas_str = ", ".join(self.horas_lista)

            if self.instance:
                self.instance.dias = dias_str
                self.instance.hora = horas_str

    def clean_fecha_alta(self):
        fecha_alta = self.cleaned_data.get('fecha_alta')
        if not fecha_alta:
            raise ValidationError("La fecha de alta es obligatoria.")
        return fecha_alta
    
    def clean(self):
        cleaned_data = super().clean()
        plan = cleaned_data.get('plan')
        fecha_alta = cleaned_data.get('fecha_alta')

        if not fecha_alta:
            self.add_error('fecha_alta', "Debes ingresar una fecha de alta válida.")

        if plan:
            # Obtener días y horas del POST
            dias = self.data.getlist('dias[]')
            horas = self.data.getlist('horas[]')

            # Verificar que los datos se estén recibiendo
            print(f"Días recibidos: {dias}")  # Para depuración
            print(f"Horas recibidas: {horas}")  # Para depuración

            if not dias or not horas:
                raise ValidationError("Debes asignar los turnos requeridos por el plan.")
            
            if len(dias) != plan.cantidad_dias:
                raise ValidationError(
                    f"El plan seleccionado requiere exactamente {plan.cantidad_dias} día(s). "
                    f"Has seleccionado {len(dias)} días."
                )
            
            if len(horas) != plan.cantidad_dias:
                raise ValidationError(
                    f"Debes asignar un horario para cada día. "
                    f"Faltan horarios para {len(dias) - len(horas)} días."
                )
            
            # Validar contenido
            for i, (dia, hora) in enumerate(zip(dias, horas), start=1):
                if not dia.strip():
                    raise ValidationError(f"El día número {i} está vacío.")
                if not hora.strip():
                    raise ValidationError(f"El horario para el día {dia} está vacío.")
            
            self.dias_lista = [dia.strip() for dia in dias]
            self.horas_lista = [hora.strip() for hora in horas]
            
            if len(set(self.dias_lista)) != len(self.dias_lista):
                raise ValidationError("No puedes asignar el mismo día más de una vez.")