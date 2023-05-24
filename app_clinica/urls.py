from django.urls import path
from . import views

app_name = 'app_clinica'
urlpatterns = [
    path('', views.home, name="home" ),
    path('agendamiento/', views.agendamiento, name="agendamiento"),
    path('registro/', views.register, name="registro"),
    path('contact/', views.contact, name="contact"),
    path('user/', views.user, name="user"),
    path('peluqueras/', views.PeluquerasLista.as_view(), name="peluqueras-lista"), #Este se utilizo de ejemplo para listar el nombre de los peluqueros
    path('editar-perfil/', views.editarPerfil, name='editar_perfil'),
    path('historial-medico/', views.historialMedico, name="historial_medico"),
    path('tus-mascotas/', views.mascotaCliente, name="mascota_cliente")

]
