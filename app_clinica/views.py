from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required , permission_required
from django.contrib.auth import authenticate, login

#importes para email
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from django.contrib import messages
from .forms import CustomUserCreationForm, AgendamientoForm, ContactoForm
from .models import Categoria, Veterinario, Peluquera

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
        
def user(request):
    return render(request,"app/user.html")   

#Este se utilizo de ejemplo para listar el nombre de los peluqueros
from django.views.generic import ListView
from django.http import JsonResponse
from .models import Peluquera

class PeluquerasLista(ListView):
    model = Peluquera

    def get(self, request, *args, **kwargs):
        peluqueras = self.get_queryset()
        data = list(peluqueras.values())
        return JsonResponse(data, safe=False)

def editarPerfil(request):
    return render(request, 'app/editar_perfil.html')

def historialMedico(request):
    return render(request, 'app/historial_clinico.html')

def mascotaCliente(request):
    return render(request, 'app/mascota_cliente.html')
