from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('entrada/',views.entrada, name='entrada'),
    path('listado/',views.listar_inventario, name='listar_inventario'),
    path('editar/<int:id>',views.editarInventario, name='editar_inventario'),
    path('eliminar/<int:id>',views.eliminarInventario, name='eliminar_inventario'),
    path('hospital/', views.inventario_por_hospital, name='inventario_por_hospital'),
]
