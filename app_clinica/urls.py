from django.urls import path
from . import views

app_name = 'app_clinica'
urlpatterns = [
    path('', views.home, name="home" ),
    path('agendamiento/', views.agendamiento, name="agendamiento"),
    path('registro/', views.register, name="registro"),

]
