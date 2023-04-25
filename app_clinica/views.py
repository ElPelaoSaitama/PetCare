from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

def home(request):
    return render(request,'app/home.html')

@login_required
def agendamiento(request):
    return render(request, 'app/home.html')

def login(request):
    return render(request,'registration/login.html'), redirect('app/home.html')

def salir(request):
    logout(request)
    return redirect('/')
    