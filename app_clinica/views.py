from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required , permission_required
from django.contrib.auth import authenticate, login
from django.forms import DateInput
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404

#importes para email
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from django.contrib import messages
from .forms import CustomUserCreationForm, AgendamientoForm, ContactoForm, ClienteForm, ChangePasswordForm, MascotaForm
from .models import Categoria, Veterinario, Peluquera, Mascota

#Importes para js del perfil
from django.views.generic import ListView
# Create your views here.

def home(request):
    data = {
        'form': ContactoForm()
    }

    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Mensaje enviado"
        else:
            data["form"] = formulario

    return render(request,'app/home.html',data)

@login_required
def agendamiento(request):
    categoria = Categoria.objects.all()
    veterinario = Veterinario.objects.all()

    data = {
        'categoria': categoria,
        'veterinario': veterinario
    }

    if request.method == 'POST':
        formulario = AgendamientoForm(request.POST, request.FILES, request=request)  # Pasa el argumento request al instanciar el formulario
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Se ha agendado la hora.')
            return redirect('app_clinica:agendamiento')  # Redirige a la misma página para generar un nuevo formulario vacío
        else:
            data["form"] = formulario
    else:
        formulario = AgendamientoForm(request=request)  # Pasa el argumento request al instanciar el formulario
        data["form"] = formulario

    return render(request, 'app/agendamiento.html', data)

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            messages.success(request, "Te has registrado correctamente")
            return redirect(to="login")
        data["form"] = formulario

    return render(request, 'registration/registro.html', data)

def contact(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        asunto = request.POST['asunto']
        mensaje = request.POST['mensaje']

        template = render_to_string('app/email_template.html', {
            'nombre' : nombre,
            'correo' : correo,
            'mensaje' : mensaje
        })

        email = EmailMessage(
          asunto,
          template,
          settings.EMAIL_HOST_USER,
          ['petcarevetter@gmail.com']
        )

        email.fail_silently = False
        email.send()

        messages.success(request,'Se ha enviado tu correo.')
        return redirect("app_clinica:home")

@login_required        
def user(request):
    return render(request,"app/user.html")   

@login_required
def historialMedico(request):
    return render(request, 'app/historial_clinico.html')

@login_required
def mascotaCliente(request):
    cliente = request.user.cliente
    mascotas = Mascota.objects.filter(dueno=cliente)
    mascotas_con_edad = [(mascota, mascota.calcular_edad()) for mascota in mascotas]
    context = {'mascotas': mascotas_con_edad}
    return render(request, 'app/mascota_cliente.html', context)


def editar_mascota(request, mascota_id):
    # Obtén la mascota a partir de su ID
    mascota = get_object_or_404(Mascota, id=mascota_id)

    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            # Redirige al usuario a la página de detalles de la mascota o a donde desees
            return redirect('/tus-mascotas/', mascota_id=mascota.id)
    else:
        form = MascotaForm(instance=mascota)

    # Establece el valor inicial del campo de fecha de nacimiento en el formulario
    form.fields['fech_naci'].widget.attrs['value'] = mascota.fech_naci.strftime('%Y-%m-%d')

    return render(request, 'app/mascota/editar_mascota.html', {'form': form})










@login_required
def editarPerfil(request):
    cliente = request.user.cliente

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            user = form.instance.user
            user.first_name = form.cleaned_data['nombre']
            user.last_name = form.cleaned_data['apellido']
            user.save()
            form.save()
            messages.success(request, 'Los cambios se guardaron correctamente.')
            return redirect('app_clinica:user')
        else:
            messages.error(request, 'Hubo un error al guardar los cambios. Por favor, verifica los datos ingresados.')
            print(form.errors)
    else:
        nombre = cliente.user.first_name
        apellido = cliente.user.last_name
        form = ClienteForm(instance=cliente, initial={'nombre': nombre, 'apellido': apellido})
        form.fields['fecha_nac'].widget = DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'birth-date', 'required': 'true'}, format='%Y-%m-%d')

    context = {'form': form}
    return render(request, 'app/editar_perfil.html', context)

@login_required
def editarPassword(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Actualizar la sesión del usuario para evitar cierre de sesión
            messages.success(request, 'Tu contraseña ha sido cambiada correctamente.')
            return redirect('app_clinica:user')
        else:
            messages.error(request, 'Hubo un error al cambiar la contraseña. Por favor, verifica los datos ingresados.')
    else:
        form = ChangePasswordForm(request.user)

    context = {'form': form}
    return render(request, 'app/change_password.html', context)




























