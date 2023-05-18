from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required , permission_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm, AgendamientoForm, ContactoForm
from .models import Categoria, Veterinario
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

#@login_required
def agendamiento(request):
    categoria = Categoria.objects.all()
    veterinario = Veterinario.objects.all()

    data = {
        'form': AgendamientoForm(),
        'categoria': categoria,
        'veterinario': veterinario
    }

    if request.method == 'POST':
        formulario = AgendamientoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Agendado"
        else:
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
