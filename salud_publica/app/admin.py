from django.contrib import admin

from.models import *



admin.site.register(Insumo)

 

admin.site.register(Hospital)
admin.site.register(Profile)


admin.site.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
  pass
  