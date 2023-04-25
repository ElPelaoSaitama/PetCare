from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home" ),
    path('agendamiento/', views.agendamiento, name="agendamiento"),
    path('login/', views.login, name="login"),
    path('salir/', views.salir, name="salir")

]
