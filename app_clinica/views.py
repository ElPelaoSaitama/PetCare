from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm
# Create your views here.

def home(request):
    return render(request,'app/home.html')
#@login_required
def agendamiento(request):
    return render(request, 'app/agendamiento.html')

def login(request):
    return render(request,'registration/login.html')

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            user = formulario.save()
            #user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data['password1'])
            #login(request,user)
            messages.success(request, "Te has registrado correctamente")
            return redirect(to="login")
        data["form"] = formulario

    return render(request, 'registration/registro.html', data)

    