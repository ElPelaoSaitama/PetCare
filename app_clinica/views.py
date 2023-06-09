from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required , permission_required
from django.contrib.auth import authenticate, login
from django.forms import DateInput
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm, AgendamientoForm, ContactoForm, ClienteForm, ChangePasswordForm, MascotaForm, AgregarMascotaForm, DiagnosticoForm, EditarAgendamientoForm
from .models import Categoria, Veterinario, Peluquera, Mascota, Agendamiento, Cliente, Agenda, Diagnostico
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, date


# importe para pdf
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

#importes para email
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

#Importes para js del perfil
from django.views.generic import ListView

from django.contrib.auth.decorators import user_passes_test


# Create your views here.
def es_veterinario(user):
    return user.groups.filter(name='Veterinarios').exists()


def home(request):
    data = {
        'form': ContactoForm(),
        'show_link' : not es_veterinario(request.user)
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
        formulario = AgendamientoForm(request.POST, request.FILES, request=request)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Se ha agendado la hora.')
            return redirect('app_clinica:agendamiento')
        else:
            data["form"] = formulario
            print(formulario.errors)  # Imprimir los errores del formulario en la consola para depuración
    else:
        formulario = AgendamientoForm(request=request)
        data["form"] = formulario

    return render(request, 'app/agendamiento.html', data)

def get_agendas(request):
    categoria_id = request.GET.get('categoria_id')
    agendas_disponibles = Agenda.objects.filter(
        categoria_id=categoria_id,
        dia__gte=timezone.now().date(),
        agendamiento__isnull=True
    )
    options = [{'id': agenda.id, 'nombre': str(agenda)} for agenda in agendas_disponibles]
    return JsonResponse(options, safe=False)

def obtener_agendas(request):
    categoria_id = request.GET.get('categoria_id')
    agendas_disponibles = Agenda.objects.filter(
        categoria_id=categoria_id,
        dia__gte=timezone.now().date(),
        agendamiento__isnull=True
    )
    options = [{'id': agenda.id, 'nombre': str(agenda)} for agenda in agendas_disponibles]
    return JsonResponse(options, safe=False)

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
    cliente = request.user.cliente
    mascotas = Mascota.objects.filter(dueno=cliente)
    consultas = Agendamiento.objects.filter(mascota__in=mascotas).order_by('-agenda__dia')

    detalles_consulta = []
    fecha_actual = date.today()

    for consulta in consultas:
        mascota_nombre = consulta.mascota.nombre
        agenda = consulta.agenda
        horario_inicio, horario_fin = agenda.get_horario_display().split(" a ")
        horario = f"{horario_inicio} a {horario_fin}"

        if agenda.dia < fecha_actual:
            detalles_consulta.append((consulta, mascota_nombre, horario, True))
        else:
            detalles_consulta.append((consulta, mascota_nombre, horario, False))

    context = {
        'detalles_consulta': detalles_consulta
    }
    return render(request, 'app/historial_clinico.html', context)

@login_required
def eliminarAgendamiento(request, consulta_id):
    consulta = get_object_or_404(Agendamiento, id=consulta_id)
    
    # Verificar si el usuario autenticado es el propietario del agendamiento
    if request.user == consulta.cliente:
        # Agregar mensaje de confirmación antes de eliminar
        messages.info(request, 'Se ha eliminado el agendamiento')
        consulta.delete()
    
    return redirect('app_clinica:historial_medico')  # Redirigir a la página del historial médico después de eliminar

@login_required
def editarAgendamiento(request, consulta_id):
    agendamiento = Agendamiento.objects.get(id=consulta_id)

    if request.method == 'POST':
        form = EditarAgendamientoForm(request.POST, instance=agendamiento, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamiento modificado exitosamente.')
            return redirect('/historial-medico/')
        else:
            print(form.errors)  # Imprimir los errores de validación del formulario
    else:
        form = EditarAgendamientoForm(instance=agendamiento, request=request)
        form.fields['agenda'].queryset = Agenda.objects.filter(categoria=agendamiento.categoria)

    print(form.errors)  # Imprimir los errores de validación del formulario antes de renderearlo

    context = {
        'form': form
    }
    return render(request, 'app/editar_agendamiento.html', context)

@login_required
def mascotaCliente(request):
    cliente = request.user.cliente
    mascotas = Mascota.objects.filter(dueno=cliente)
    context = {'mascotas': mascotas}
    return render(request, 'app/mascota_cliente.html', context)

@login_required
def editar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Los datos de la mascota se han actualizado correctamente.')
            return redirect('/tus-mascotas/', mascota_id=mascota.id)
        else:
            messages.error(request, 'No se pudieron actualizar los datos de la mascota. Por favor, verifica los datos ingresados.')
    else:
        form = MascotaForm(instance=mascota)

    form.fields['fech_naci'].widget.attrs['value'] = mascota.fech_naci.strftime('%Y-%m-%d')

    return render(request, 'app/mascota/editar_mascota.html', {'form': form})


@login_required
def generar_pdf(request, mascota_id):
    # Obtén la mascota a partir de su ID
    mascota = get_object_or_404(Mascota, id=mascota_id)

    # Obtén los diagnósticos asociados a la mascota
    diagnosticos = Diagnostico.objects.filter(agendamiento__mascota=mascota)

    # Crea un objeto BytesIO para almacenar el PDF generado
    buffer = BytesIO()

    # Establece el tamaño de página y márgenes
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=inch/2, leftMargin=inch/2, topMargin=inch/2, bottomMargin=inch/2)

    # Lista para almacenar los elementos del PDF
    elements = []

    # Estilos para el título y el contenido
    styles = getSampleStyleSheet()
    estilo_titulo = styles['Title']
    estilo_contenido = styles['BodyText']

    # Agrega el título al PDF
    titulo = f'Ficha de mascota - {mascota.nombre.capitalize()}'
    elements.append(Paragraph(titulo, estilo_titulo))
    elements.append(Spacer(1, 0.5*inch))

    # Agrega la imagen al PDF
    ruta_imagen = 'app_clinica/static/app/img/LogoPetCare.png'  # Ruta de la imagen
    imagen = Image(ruta_imagen, width=2*inch, height=2*inch)
    elements.append(imagen)
    elements.append(Spacer(1, 0.5*inch))

    # Agrega los campos de la mascota al PDF
    dueno_nombre = f'Dueño: {mascota.dueno.user.first_name.capitalize()} {mascota.dueno.user.last_name.capitalize()}'
    especie = f'Especie: {mascota.especie}'
    raza = f'Raza: {mascota.raza}'
    sexo = f'Sexo: {mascota.get_sexo_display()}'
    fecha_nacimiento = f'Fecha de Nacimiento: {mascota.fech_naci}'
    microchip = f'Microchip: {mascota.microchip}'

    elements.append(Paragraph(dueno_nombre, estilo_contenido))
    elements.append(Spacer(1, 0.25*inch))
    elements.append(Paragraph(especie, estilo_contenido))
    elements.append(Spacer(1, 0.25*inch))
    elements.append(Paragraph(raza, estilo_contenido))
    elements.append(Spacer(1, 0.25*inch))
    elements.append(Paragraph(sexo, estilo_contenido))
    elements.append(Spacer(1, 0.25*inch))
    elements.append(Paragraph(fecha_nacimiento, estilo_contenido))
    elements.append(Spacer(1, 0.25*inch))
    elements.append(Paragraph(microchip, estilo_contenido))
    elements.append(Spacer(1, 0.5*inch))

    # Agrega los diagnósticos al PDF
    elements.append(Paragraph("Diagnósticos:", estilo_titulo))
    for diagnostico in diagnosticos:
        agendamiento = diagnostico.agendamiento
        agenda = agendamiento.agenda
        fecha_agendamiento = agenda.dia.strftime('%d/%m/%Y')
        nombre_veterinario = ""
        if agenda.veterinario:
            nombre_veterinario = agenda.veterinario.user.get_full_name()
        elements.append(Spacer(1, 0.25*inch))



        # Agrega fecha de agendamiento y veterinario
        elements.append(Paragraph(f"Fecha de Agendamiento: {fecha_agendamiento}", estilo_contenido))
        elements.append(Paragraph(f"Veterinario: {nombre_veterinario}", estilo_contenido))

        # Agrega el texto del diagnóstico
        elements.append(Spacer(1, 0.25*inch))
        diagnostico_texto = f"Diagnóstico: {diagnostico.diagnostico}"
        elements.append(Paragraph(diagnostico_texto, estilo_contenido))





    # Genera el PDF
    doc.build(elements)

    # Vuelve al inicio del objeto BytesIO
    buffer.seek(0)

    # Crea una respuesta de archivo para descargar el PDF
    return FileResponse(buffer, as_attachment=True, filename=f'Ficha-{mascota.nombre.capitalize()}.pdf')

@login_required
def agregarMascota(request):
    if request.method == 'POST':
        form = AgregarMascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.dueno = request.user.cliente
            mascota.save()
            messages.success(request, 'La mascota se ha guardado correctamente.')
            return redirect('/tus-mascotas/')
        else:
            messages.error(request, 'No se pudo guardar la mascota. Por favor, verifica los datos ingresados.')
    else:
        form = AgregarMascotaForm()
    
    context = {'form': form}
    return render(request, 'app/mascota/agregar_mascota.html', context)

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

def colaborador_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.groups.filter(name='Veterinarios').exists():
            login(request, user)
            return redirect('app_clinica:colaborador')  # Redirige a la página de inicio del colaborador
        else:
            # Manejar error de inicio de sesión
            return render(request, 'app/colaboradores/colaborador_login.html', {'error': 'Credenciales inválidas'})
    else:
        return render(request, 'app/colaboradores/colaborador_login.html')


# Seccion solo para colaboradores

@login_required      
def colaborador(request):
    return render(request,"app/colaboradores/dashboard_colaborador.html")



# Seccion solo para veterinarios

def is_veterinario(user):
    return user.groups.filter(name='Veterinarios').exists()

@login_required
@user_passes_test(is_veterinario)
def citasColaborador(request):
    veterinario = request.user.veterinario  # Obtener el veterinario actualmente logeado
    agendamientos = Agendamiento.objects.select_related('mascota', 'categoria', 'agenda').filter(agenda__veterinario=veterinario)

    for agendamiento in agendamientos:
        agendamiento.tiene_diagnostico = agendamiento.diagnostico_set.exists()

    return render(request, "app/colaboradores/citas_colaborador.html", {'agendamientos': agendamientos})

@login_required
@user_passes_test(is_veterinario)
def diagnostico(request, consulta_id):
    agendamiento = Agendamiento.objects.get(id=consulta_id)

    if request.method == 'POST':
        form = DiagnosticoForm(request.POST)  # Inicializa el formulario con los datos recibidos
        if form.is_valid():
            diagnostico_text = form.cleaned_data['diagnostico']
            veterinario = request.user
            
            # Crea una instancia de Diagnostico y guárdala en la base de datos
            diagnostico = Diagnostico(agendamiento=agendamiento, diagnostico=diagnostico_text, veterinario=veterinario)
            diagnostico.save()
            
            # Agrega un mensaje de éxito
            messages.success(request, 'El diagnóstico se guardó correctamente.')
            
            # Redirige al usuario a la página de detalles del agendamiento o a donde desees
            return redirect('/citas-colaborador/')
            
    else:
        form = DiagnosticoForm()  # Crea una instancia vacía del formulario

    context = {
        'agendamiento': agendamiento,
        'form': form,  # Agrega el formulario al contexto
    }
    return render(request, 'app/colaboradores/diagnostico.html', context)



































