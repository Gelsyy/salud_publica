from django.shortcuts import render,redirect, get_object_or_404
from .forms import InventarioForm
from .forms import EditarForm
from .models import Inventario, Hospital, Insumo
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_GET

def error(request):
    return render(request, 'error.html')

def login(request):
    return render(request, 'login.html')
  

def aumentar_salidas(request, id_inventario):
    inventario = get_object_or_404(Inventario, id_inventario=id_inventario)

    if request.method == 'POST':
        cantidad_salida = int(request.POST.get('cantidad_salida', 0))
        if cantidad_salida <= inventario.cantidad_entrada:
            inventario.cantidad_salida += cantidad_salida
            inventario.save() 
            return redirect('detalles_inventario_hospital', id_hospital=inventario.id_hospital_id)
    return redirect('error') 

def eliminarInventario(request, id):
    try:
        entrada = Inventario.objects.get(id_inventario=id)
        id_hospital = entrada.id_hospital.id_hospital
        entrada.delete()
    except Inventario.DoesNotExist:
      
        return redirect('pagina_de_error')  

    return redirect('detalles_inventario_hospital', id_hospital=id_hospital)

def entrada(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('entrada') 
    else:
        form = InventarioForm()

    return render(request, 'entrada.html', {'form': form})



def listar_hospitales(request):
    hospitales = Hospital.objects.all()
    return render(request, 'central.html', {'hospitales': hospitales})


def detalles_inventario_hospital(request, id_hospital):
    hospital = get_object_or_404(Hospital, id_hospital=id_hospital)
    inventarios = hospital.inventario_set.all()

    # Obtener parámetros de búsqueda del formulario GET
    lote_query = request.GET.get('lote')
    insumo_id = request.GET.get('insumo_nombre')  # Cambiar a insumo_id para usar el ID del insumo

    # Filtrar por nombre de insumo si se proporcionó
    if insumo_id:
        inventarios = inventarios.filter(id_insumo=insumo_id)

    # Filtrar por lote si se proporcionó
    if lote_query:
        inventarios = inventarios.filter(lote__icontains=lote_query)

    # Obtener todos los insumos para el formulario de selección
    nombre_insumos = Insumo.objects.all()

    context = {
        'hospital': hospital,
        'inventarios': inventarios,
        'nombre_insumos': nombre_insumos,  # Pasar la lista de insumos al contexto
        'lote_query': lote_query,
        'insumo_id': insumo_id,  # Pasar el ID del insumo seleccionado
    }
    return render(request, 'listar_hospital.html', context)


