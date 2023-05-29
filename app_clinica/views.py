from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required , permission_required
from django.contrib.auth import authenticate, login
from django.forms import DateInput
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm, AgendamientoForm, ContactoForm, ClienteForm, ChangePasswordForm, MascotaForm, AgregarMascotaForm
from .models import Categoria, Veterinario, Peluquera, Mascota

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

@login_required
def historialMedico(request):
    return render(request, 'app/historial_clinico.html')

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
    elements.append(Paragraph(especie, estilo_contenido))
    elements.append(Paragraph(raza, estilo_contenido))
    elements.append(Paragraph(sexo, estilo_contenido))
    elements.append(Paragraph(fecha_nacimiento, estilo_contenido))
    elements.append(Paragraph(microchip, estilo_contenido))

    # Agrega espacio adicional
    elements.append(Spacer(1, 0.5*inch))

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




























