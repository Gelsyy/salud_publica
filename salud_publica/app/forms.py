from django import forms
from .models import Inventario, Insumo, Hospital

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['lote', 'id_insumo', 'id_hospital', 'cantidad_entrada', 'fecha_vencimiento', 'fecha_entrada']
        widgets = {
            'id_insumo': forms.Select(attrs={'class': 'form-control'}),
            'id_hospital': forms.Select(attrs={'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_entrada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_hospital'].queryset = Hospital.objects.all()
        self.fields['id_insumo'].queryset = Insumo.objects.all()


class EditarForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['lote', 'cantidad_entrada', 'cantidad_salida', 'fecha_vencimiento', 'fecha_entrada']