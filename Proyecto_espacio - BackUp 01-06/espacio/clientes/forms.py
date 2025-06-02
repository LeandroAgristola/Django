from django import forms
from .models import Cliente, Plan
from calendario.models import Turno
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import F, Q
from datetime import datetime, timedelta

class ClienteForm(forms.ModelForm):
    """
    Formulario para crear/editar clientes con validaciones personalizadas.
    - Maneja asignación de turnos
    - Valida unicidad de DNI y email
    - Verifica disponibilidad de turnos
    """
    
    # Campos ocultos para manejar días y horarios
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
        """Inicialización que procesa días y horarios seleccionados"""
        self.dias_lista = []
        self.horas_lista = []
        super().__init__(*args, **kwargs)

        
        # Procesar datos de días/horarios del request
        data = args[0] if args else None
        if data:
            self.dias_lista = data.getlist('dias[]')
            self.horas_lista = data.getlist('horas[]')

            dias_str = ", ".join(self.dias_lista)
            horas_str = ", ".join(self.horas_lista)

            if self.instance:
                self.instance.dias = dias_str
                self.instance.hora = horas_str

    def clean_dni(self):
        """Validación de DNI único"""
        dni = self.cleaned_data.get('dni')
        if dni is not None:
            qs = Cliente.objects.filter(dni=dni)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Ya existe un cliente con ese DNI.")
        return dni

    def clean_mail(self):
        """Validación de email único"""
        mail = self.cleaned_data.get('mail')
        if mail:
            qs = Cliente.objects.filter(mail=mail)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Ya existe un cliente con ese email.")
        return mail

    def clean_fecha_alta(self):
        """Validación de fecha de alta obligatoria"""
        fecha_alta = self.cleaned_data.get('fecha_alta')
        if not fecha_alta:
            raise ValidationError("La fecha de alta es obligatoria.")
        return fecha_alta
    
    def clean(self):
        """
        Validaciones complejas:
        - Verifica asignación correcta de turnos según plan
        - Valida disponibilidad de turnos seleccionados en el mes siguiente
        - Evita duplicados en días/horarios
        """
        from calendario.models import Turno  # Asegurate de tener este import también al inicio del archivo

        cleaned_data = super().clean()
        plan = cleaned_data.get('plan')
        fecha_alta = cleaned_data.get('fecha_alta')

        if not fecha_alta:
            self.add_error('fecha_alta', "Debes ingresar una fecha de alta válida.")
            return

        if plan:
            dias = self.data.getlist('dias[]')
            horas = self.data.getlist('horas[]')

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

            for i, (dia, hora) in enumerate(zip(dias, horas), start=1):
                if not dia.strip():
                    raise ValidationError(f"El día número {i} está vacío.")
                if not hora.strip():
                    raise ValidationError(f"El horario para el día {dia} está vacío.")

            self.dias_lista = [dia.strip() for dia in dias]
            self.horas_lista = [hora.strip() for hora in horas]

            turnos_combinados = list(zip(self.dias_lista, self.horas_lista))
            if len(turnos_combinados) != len(set(turnos_combinados)):
                raise ValidationError("No puedes asignar el mismo día y hora más de una vez.")

            # Validar turnos futuros
            dias_esp = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

            for dia, hora in zip(self.dias_lista, self.horas_lista):
                try:
                    dia_idx = dias_esp.index(dia.lower())
                    hora_dt = datetime.strptime(hora, "%H:%M").time()

                    proximo_mes_inicio = (fecha_alta.replace(day=28) + timedelta(days=4)).replace(day=1)
                    fin_periodo_chequeo = (proximo_mes_inicio.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
                    fecha_iteracion = fecha_alta 

                    while fecha_iteracion <= fin_periodo_chequeo:
                        if fecha_iteracion.weekday() == dia_idx:
                            ocupados = Turno.objects.filter(
                                fecha=fecha_iteracion,
                                hora=hora_dt
                            ).filter(
                                Q(cliente__fecha_alta__lte=F('fecha')) &
                                (Q(cliente__fecha_baja__isnull=True) | Q(cliente__fecha_baja__gte=F('fecha')))
                            ).count()

                            if ocupados >= 6:
            
                                is_own_slot_no_change = False
                                if self.instance and self.instance.pk:
                                    client_dias = [d.strip().lower() for d in (self.instance.dias or "").split(',')]
                                    client_horas = [h.strip() for h in (self.instance.hora or "").split(',')]
                                    if dia.lower() in client_dias and hora in client_horas:
                                        if Turno.objects.filter(fecha=fecha_iteracion, hora=hora_dt, cliente=self.instance).exists():
                                            if ocupados == 6: 
                                                is_own_slot_no_change = True 
                                
                                if not is_own_slot_no_change: 
                                    raise ValidationError(
                                        f"El horario {hora} de los {dia.capitalize()} estará completo a partir del {fecha_iteracion.strftime('%d/%m/%Y')}."
                                    )
                        fecha_iteracion += timedelta(days=1)

                except ValueError: 
                    self.add_error(None, f"Se encontró un día ('{dia}') u hora ('{hora}') con formato inválido durante la validación de turnos.") 


