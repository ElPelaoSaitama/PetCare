from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Agendamiento, Categoria , Veterinario, Peluquera, Contacto, Mascota, Agenda

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


class AgendamientoForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'style': 'text-transform: uppercase;', 'disabled': 'disabled'}))
    apellido = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'style': 'text-transform: uppercase;', 'disabled': 'disabled'}))
    rut = forms.CharField(max_length=12, required=True, widget=forms.TextInput(attrs={'class': 'form-control rut-input'}))
    correo = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly','disabled': 'disabled'}))
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    agenda = forms.ModelChoiceField(queryset=Agenda.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True)
    mascota = forms.ModelChoiceField(queryset=Mascota.objects.none(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request:
            user = self.request.user
            self.fields['nombre'].widget.attrs['value'] = user.first_name
            self.fields['nombre'].initial = user.first_name

            self.fields['apellido'].widget.attrs['value'] = user.last_name
            self.fields['apellido'].initial = user.last_name

            self.fields['correo'].widget.attrs['value'] = user.email
            self.fields['correo'].initial = user.email

            self.fields['mascota'].queryset = Mascota.objects.filter(dueno__user=self.request.user)

        self.fields['cliente'].widget = forms.HiddenInput()
        self.fields['cliente'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request:
            user = self.request.user
            instance.cliente_id = user.id
            instance.nombre = user.first_name
            instance.apellido = user.last_name
            instance.correo = user.email
            instance.cliente = user
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Agendamiento
        fields = '__all__'









class ContactoForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'nombre', 'name': 'nombre'}))
    correo = forms.EmailField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'correo', 'name': 'correo'}))
    asunto = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'asunto', 'name': 'asunto'}))
    mensaje = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'mensaje', 'name': 'mensaje'}))


    class Meta:
        model = Contacto
        fields = '__all__'


# Codigo antiguo para el fomulario de registro de usuario

"""class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=50, required=True, label="Correo", widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, label="Nombre", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, label="Apellido", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Contraseña", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña', 'id': 'id_password1', 'autocomplete': 'off'}))
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña', 'id': 'id_password2', 'autocomplete': 'off'}))
    
    class Meta:
        model = User
        fields = ['email','first_name', 'last_name']"""