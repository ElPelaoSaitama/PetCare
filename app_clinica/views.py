from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request,'app/home.html')

def agendamiento(request):
    return render(request, 'app/agendamiento.html')
    