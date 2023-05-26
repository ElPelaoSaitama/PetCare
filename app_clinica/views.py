from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required , permission_required
from django.contrib.auth import authenticate, login

#importes para email
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from django.contrib import messages
from .forms import CustomUserCreationForm, AgendamientoForm, ContactoForm, ClienteForm
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

@login_required        
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

"""@login_required
def editarPerfil(request):
    return render(request, 'app/editar_perfil.html')"""

@login_required
def historialMedico(request):
    return render(request, 'app/historial_clinico.html')

@login_required
def mascotaCliente(request):
    return render(request, 'app/mascota_cliente.html')


#test para editar perfil

from django.forms import DateInput

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



























