from django import forms
from .models import Inventario

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields=['lote', 'id_insumo', 'id_hospital', 'cantidad_entrada', 'fecha_vencimiento', 'fecha_entrada']

class EditarForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields=['lote', 'id_insumo', 'id_hospital', 'cantidad_entrada', 'cantidad_salida', 'fecha_vencimiento', 'fecha_entrada']