from django.shortcuts import render,redirect, get_object_or_404
from .forms import InventarioForm
from .forms import EditarForm
from .models import Inventario, Hospital
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    return render(request, 'home.html')

def entrada(request):
    if request.method=='POST':
        entrada_form = InventarioForm(request.POST)
        if entrada_form.is_valid():
            entrada_form.save()
            return redirect('home')
    else:    
       entrada_form = InventarioForm()
       
    return render(request, 'entrada.html', {'entrada_form':entrada_form}) 

def listar_inventario(request):
    inventarios=Inventario.objects.all()
    return render(request, 'listar_inventario.html', {'inventarios':inventarios})


def editarInventario(request, id):
    entrada_form = None 
    error = None 

    try:
        entrada = Inventario.objects.get(id_inventario = id) 
        if request.method == 'GET':
            entrada_form = EditarForm(instance=entrada)
        else:
            entrada_form = EditarForm(request.POST, instance=entrada)
            if entrada_form.is_valid():
                entrada_form.save()
                return redirect('editar_inventario', id)  
    except Inventario.DoesNotExist as e:
        error = e 
    return render(request, 'entrada.html', {'entrada_form': entrada_form, 'error': error})    
    
def eliminarInventario(request, id):
    inventario= Inventario.objects.get(id_inventario=id)      
    inventario.delete()
    return redirect('listar_inventario')



def inventario_por_hospital(request):
   
    hospitales = Hospital.objects.all()

    if request.method == 'POST':
        hospital_id = request.POST['hospital_id']
        hospital = Hospital.objects.get(id_hospital=hospital_id)
        inventarios = Inventario.objects.filter(id_hospital=hospital)
                
        context = {
            'hospitales': hospitales,
            'inventarios': inventarios
        }
                
        return render(request, 'inventario.html', context)

    

    