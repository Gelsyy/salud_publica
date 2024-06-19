from django.contrib import admin

# Register your models here.
from.models import Insumo
from.models import Hospital
from.models import Inventario


admin.site.register(Insumo)
admin.site.register(Hospital)

admin.site.register(Inventario)