from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_backends
from .models import PerfilUsuario, Punto, Envase, Bono, CategoriaEnvase
from .forms import RegistroForm, RegistroEnvaseForm, BuscarUsuarioForm
from datetime import datetime
from django.db.models import Sum

def pagina_principal(request):
    usuario = None
    total_puntos = 0
    es_admin = request.user.is_staff if request.user.is_authenticated else False

    if request.user.is_authenticated:
        try:
            usuario = request.user.perfilusuario
            # Calcular el total de puntos directamente desde la base de datos
            total_puntos = Punto.objects.filter(usuario=usuario).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
        except PerfilUsuario.DoesNotExist:
            usuario = None

    return render(request, 'pagina_principal.html', {
        'usuario': usuario,
        'total_puntos': total_puntos,
        'es_admin': es_admin,
    })

def lista_usuarios(request):
    usuarios = PerfilUsuario.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def es_administrador(user):
    return user.is_staff

@login_required
@user_passes_test(es_administrador)
def buscar_usuario(request):
    form = BuscarUsuarioForm(request.POST or None)
    usuario = None

    if form.is_valid():
        cedula = form.cleaned_data['cedula_usuario']
        usuario = get_object_or_404(PerfilUsuario, cedula=cedula)

    return render(request, 'buscar_usuario.html', {'form': form, 'usuario': usuario})

@login_required
@user_passes_test(es_administrador)
def perfil_usuario(request, usuario_id):
    usuario = get_object_or_404(PerfilUsuario, id=usuario_id)
    puntos = Punto.objects.filter(usuario=usuario)
    bonos = []  # Si tienes lógica para los bonos, inclúyela aquí

    # Calcular el total de puntos
    total_puntos = sum(punto.cantidad for punto in puntos)

    return render(request, 'perfil_usuario.html', {
        'usuario': usuario,
        'puntos': puntos,
        'bonos': bonos,
        'total_puntos': total_puntos,  # Pasar el total al contexto
    })

@login_required
@user_passes_test(lambda u: u.is_staff)  # Solo administradores pueden registrar envases
def registrar_envases(request, usuario_id):
    usuario = get_object_or_404(PerfilUsuario, id=usuario_id)

    # Variables para almacenar los datos de la sesión
    if 'envases_registrados' not in request.session:
        request.session['envases_registrados'] = []  # Lista de envases registrados en la sesión
        request.session['puntos_acumulados'] = 0  # Puntos acumulados en la sesión

    envases_registrados = request.session['envases_registrados']
    puntos_acumulados = request.session['puntos_acumulados']

    if request.method == 'POST':
        form = RegistroEnvaseForm(request.POST)
        if form.is_valid():
            categoria = form.cleaned_data['categoria']

            # Registrar el envase en la sesión
            envase = {
                'numero': len(envases_registrados) + 1,
                'hora': datetime.now().strftime('%H:%M:%S'),
                'categoria': str(categoria),
                'puntos': categoria.puntos_asignados,
            }
            envases_registrados.append(envase)
            puntos_acumulados += categoria.puntos_asignados

            # Actualizar la sesión
            request.session['envases_registrados'] = envases_registrados
            request.session['puntos_acumulados'] = puntos_acumulados

            # Limpiar el formulario para registrar otro envase
            form = RegistroEnvaseForm()
    else:
        form = RegistroEnvaseForm()

    if 'guardar' in request.POST:
        # Guardar los puntos acumulados al usuario
        for envase in envases_registrados:
            categoria = CategoriaEnvase.objects.get(nombre_categoria=envase['categoria'].split(':')[0])
            Envase.objects.create(
                tamaño=0,  # No se especifica el tamaño en este flujo
                usuario=usuario,
                categoria=categoria,
            )
        # Registrar los puntos acumulados como una sola transacción
        if puntos_acumulados > 0:
            Punto.objects.create(usuario=usuario, cantidad=puntos_acumulados)

        # Limpiar la sesión
        request.session['envases_registrados'] = []
        request.session['puntos_acumulados'] = 0

        return redirect('perfil_usuario', usuario_id=usuario.id)

    return render(request, 'registrar_envases.html', {
        'form': form,
        'usuario': usuario,
        'puntos_acumulados': puntos_acumulados,
        'envases_registrados': envases_registrados,
        'puntos_totales': sum(p.cantidad for p in Punto.objects.filter(usuario=usuario)),
    })

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Obtener el backend de autenticación
            backend = get_backends()[0]
            user.backend = f'{backend.__module__}.{backend.__class__.__name__}'
            login(request, user)
            return redirect('pagina_principal')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def perfil_usuario_actual(request):
    usuario = request.user.perfilusuario
    puntos = Punto.objects.filter(usuario=usuario)

    # Calcular el total de puntos directamente desde la base de datos
    total_puntos = puntos.aggregate(Sum('cantidad'))['cantidad__sum'] or 0

    print(f"Puntos del usuario {usuario.cedula}: {puntos}")
    print(f"Total de puntos: {total_puntos}")

    bonos = Bono.objects.filter(usuario=usuario)
    return render(request, 'perfil_usuario.html', {
        'usuario': usuario,
        'puntos': puntos,
        'bonos': bonos,
        'total_puntos': total_puntos,  # Pasar el total al contexto
    })
