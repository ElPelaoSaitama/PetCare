from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Agendamiento, Categoria , Veterinario, Peluquera, Contacto, Mascota, Agenda, Cliente, Genero, Especie, Raza
from django.forms.widgets import DateInput
from django.forms import DateInput
from django.contrib.auth.forms import PasswordChangeForm
from datetime import date
from django.db.models import Q
from django.utils import timezone

User = get_user_model()

class CustomLogin(AuthenticationForm):
    username = forms.EmailField(required=True, label=("Correo"), widget=forms.TextInput(attrs={'placeholder': 'example@example.com','class': 'form-control '}))
    password = forms.CharField(required=True, label=("Contraseña"), widget=forms.PasswordInput(attrs={'placeholder': '*****','class': 'form-control '}))

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Correo electrónico"),
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    first_name = forms.CharField(
        max_length=30,
        required=True,
        label=_("Nombre"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        label=_("Apellido"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

    password2 = forms.CharField(
        label=_("Confirmar contraseña"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

from django import forms
from django.utils import timezone
from django.db.models import Q

class AgendamientoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    agenda = forms.ModelChoiceField(queryset=Agenda.objects.none(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)
    mascota = forms.ModelChoiceField(queryset=Mascota.objects.none(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request:
            self.fields['mascota'].queryset = Mascota.objects.filter(dueno__user=self.request.user)

        self.fields['agenda'].queryset = Agenda.objects.none()

        if self.is_bound and 'categoria' in self.data:
            categoria_id = self.data['categoria']
            agendas_disponibles = Agenda.objects.filter(
                Q(categoria=categoria_id) &
                Q(dia__gte=timezone.now().date()) &
                Q(agendamiento__isnull=True)
            )
            self.fields['agenda'].queryset = agendas_disponibles
        elif self.instance.pk:
            categoria_id = self.instance.categoria_id
            agendas_disponibles = Agenda.objects.filter(
                Q(categoria=categoria_id) &
                Q(dia__gte=timezone.now().date()) &
                Q(agendamiento__isnull=True)
            )
            self.fields['agenda'].queryset = agendas_disponibles
            self.initial['agenda'] = self.instance.agenda_id

    def clean_categoria(self):
        categoria = self.cleaned_data['categoria']
        if categoria:
            return categoria
        else:
            raise forms.ValidationError('Debe seleccionar una categoría.')

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request:
            user = self.request.user
            instance.cliente = user
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Agendamiento
        exclude = ['cliente']

class ContactoForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'nombre', 'name': 'nombre'}))
    correo = forms.EmailField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'correo', 'name': 'correo'}))
    asunto = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'asunto', 'name': 'asunto'}))
    mensaje = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'mensaje', 'name': 'mensaje'}))

    class Meta:
        model = Contacto
        fields = '__all__'

class ClienteForm(forms.ModelForm):
    genero = forms.ModelChoiceField(queryset=Genero.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'id': 'genero'}))
    cellNumber = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'cellNumber', 'placeholder': 'Número de nueve dígitos'}))
    direccion = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'direccion'}))
    rut = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'rut'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'required': True, 'readonly': True, 'style': 'background-color: lightgray;'}))
    nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'nombre', 'required': 'true'}))
    apellido = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'last-name', 'required': 'true'}))
    fecha_nac = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'birth-date', 'required': 'true'}))

    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'genero', 'cellNumber', 'direccion', 'rut', 'email', 'fecha_nac']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].initial = self.instance.user.first_name
        self.fields['apellido'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email
        self.fields['fecha_nac'].initial = self.instance.fecha_nac

    def clean_cellNumber(self):
        cellNumber = self.cleaned_data['cellNumber']
        if len(str(cellNumber)) != 9:
            raise forms.ValidationError('El número de celular debe tener 9 dígitos.')
        return cellNumber

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'

class MascotaForm(forms.ModelForm):
    fech_naci = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'birth-date', 'required': 'true'}))

    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'sexo', 'fech_naci', 'microchip']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'id': 'nombre', 'required': 'true'}),
            'especie': forms.Select(attrs={'class': 'form-control', 'id': 'especie', 'required': 'true'}),
            'raza': forms.Select(attrs={'class': 'form-control', 'id': 'raza', 'required': 'true'}),
            'sexo': forms.Select(attrs={'class': 'form-control', 'id': 'genero'}),
            'microchip': forms.NumberInput(attrs={'class': 'form-control', 'id': 'microchip'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.fech_naci:
            self.initial['fech_naci'] = self.instance.fech_naci.strftime('%Y-%m-%d')

class AgregarMascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'sexo', 'fech_naci', 'microchip']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'id': 'nombre', 'required': 'true', 'placeholder': 'Nombre de su mascota'}),
            'especie': forms.Select(attrs={'class': 'form-control', 'id': 'especie', 'required': 'true'}),
            'raza': forms.Select(attrs={'class': 'form-control', 'id': 'raza', 'required': 'true'}),
            'sexo': forms.Select(attrs={'class': 'form-control', 'id': 'genero'}),
            'microchip': forms.NumberInput(attrs={'class': 'form-control', 'id': 'microchip', 'placeholder': 'Si no tiene chip, déjelo en cero'}),
            'fech_naci': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'fecha_nac', 'required': 'true'})
        }

class EditarAgendamientoForm(forms.ModelForm):
    class Meta:
        model = Agendamiento
        fields = ['mascota', 'categoria', 'agenda', 'mensaje']
        widgets = {
            'mascota': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'agenda': forms.Select(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request and self.request.user.is_authenticated:
            user = self.request.user
            cliente = Cliente.objects.get(user=user)
            self.fields['mascota'].queryset = Mascota.objects.filter(dueno=cliente)

        if self.is_valid():  # Verificar si el formulario es válido
            # Obtener la categoría seleccionada si ya está asignada al agendamiento
            categoria_id = self.instance.categoria_id if self.instance.pk else None

            if categoria_id:
                # Filtrar las agendas disponibles según la categoría seleccionada
                agendas_disponibles = Agenda.objects.filter(
                    Q(categoria=categoria_id) &
                    Q(dia__gte=timezone.now().date()) &
                    Q(agendamiento__isnull=True)
                )
                self.fields['agenda'].queryset = agendas_disponibles

        # Establecer el valor inicial del campo 'agenda' si ya está asignada
        if self.instance.pk:
            self.fields['agenda'].initial = self.instance.agenda






from django import forms
from .models import Diagnostico

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['diagnostico']





































