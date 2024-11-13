from django.shortcuts import render,redirect, get_object_or_404
from .forms import InventarioForm
from .forms import EditarForm
from .models import Inventario, Hospital, Insumo, Profile
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from datetime import timedelta


@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')



@login_required
def redirect_after_login(request):
    profile = getattr(request.user, 'profile', None)
    
    if profile and profile.hospital:
        # Redirige a detalles del inventario del hospital asociado
        return redirect('detalles_inventario_hospital', id_hospital=profile.hospital.id_hospital)
    else:
        # Redirige al listado de hospitales si no hay hospital asociado
        return redirect('listar_hospitales')

@login_required
def error(request, id_hospital=None):
    context = {'id_hospital': id_hospital}
    return render(request, 'error.html', context)


  

@login_required
def aumentar_salidas(request, id_inventario):
    inventario = get_object_or_404(Inventario, id_inventario=id_inventario)

    if request.method == 'POST':
        cantidad_salida = int(request.POST.get('cantidad_salida', 0))
        if cantidad_salida <= inventario.existencia:
            inventario.cantidad_salida += cantidad_salida
            inventario.save() 
            return redirect('detalles_inventario_hospital', id_hospital=inventario.id_hospital_id)
        else:
            # Redirigir a la vista de error con el ID del hospital
            return redirect('error', id_hospital=inventario.id_hospital_id)

    # Si no es un método POST o si hay otro tipo de error, redirigir a la vista de error
    return redirect('error')


@login_required
def eliminarInventario(request, id):
    try:
        entrada = Inventario.objects.get(id_inventario=id)
        id_hospital = entrada.id_hospital.id_hospital
        entrada.delete()
    except Inventario.DoesNotExist:
      
        return redirect('pagina_de_error')  

    return redirect('detalles_inventario_hospital', id_hospital=id_hospital)


@login_required
def entrada(request, id_hospital):
    hospital = get_object_or_404(Hospital, id_hospital=id_hospital)

    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            inventario = form.save(commit=False)
            inventario.id_hospital = hospital
            inventario.save()
            messages.success(request, 'Se agregó correctamente.')
            return redirect('entrada', id_hospital=id_hospital)
        else:
            messages.error(request, 'No se pudo agregar. Por favor, revisa los datos.')
    else:
        form = InventarioForm()

    context = {
        'form': form,
        'hospital': hospital,
    }

    return render(request, 'entrada.html', context)

@login_required
def listar_hospitales(request):
    hospitales = Hospital.objects.all()
    return render(request, 'central.html', {'hospitales': hospitales})



def detalles_inventario_hospital(request, id_hospital):
    hospital = get_object_or_404(Hospital, id_hospital=id_hospital)
    inventarios = hospital.inventario_set.all()
    today = timezone.now().date()
    try:
        profile=Profile.objects.get(user=request.user)
        if profile.hospital != hospital:
            return HttpResponseForbidden("NO TIENE PERMISO PARA ACCEDER A ESTE INVENTARIO")
    except Profile.DoesNotExist:
        pass    

    # Obtener parámetros de búsqueda del formulario GET
    lote_query = request.GET.get('lote')
    insumo_id = request.GET.get('insumo_nombre')  
    fecha = request.GET.get('fecha_entrada')
    filtro = request.GET.get('filtro')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
   
   
    if fecha_inicio and fecha_fin:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        inventarios = inventarios.filter(fecha_entrada__range=(fecha_inicio, fecha_fin))
    
    # Filtrar por nombre de insumo si se proporcionó
    if insumo_id:
        inventarios = inventarios.filter(id_insumo=insumo_id)

     # Filtrar por nombre de fechca si se proporcionó
    if fecha:
        inventarios = inventarios.filter(fecha_entrada=fecha)     
     # Filtrar por lote si se proporcionó
    if lote_query:
        inventarios = inventarios.filter(lote__icontains=lote_query)   
   
    if filtro == 'proximo_vencer':
        fecha_hoy = timezone.now().date()
        fecha_limite = fecha_hoy + timedelta(days=15)
        inventarios = inventarios.filter(fecha_vencimiento__range=(fecha_hoy, fecha_limite))
    elif filtro == 'vencidos':
        fecha_hoy = timezone.now().date()
        inventarios = inventarios.filter(fecha_vencimiento__lt=fecha_hoy)
    elif filtro == 'cobertura_critica':
         inventarios = [inv for inv in inventarios if inv.cobertura_field < 15] 
    elif filtro == 'cobertura_limite':
        inventarios = [inv for inv in inventarios if inv.cobertura_field == 15]
    # Obtener todos los insumos para el formulario de selección
    nombre_insumos = Insumo.objects.all()

    context = {
        'hospital': hospital,
        'inventarios': inventarios,
        'nombre_insumos': nombre_insumos,  
        'lote_query': lote_query,
        'insumo_id': insumo_id,  
        'today': today,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    return render(request, 'listar_hospital.html', context)

