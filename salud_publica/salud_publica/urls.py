from django.contrib import admin
from django.urls import path
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('aumentar_salidas/<int:id_inventario>/', views.aumentar_salidas, name='aumentar_salidas'),
    path('entrada/', views.entrada, name='entrada'),
    path('', views.login, name='login'),
    path('error/', views.error, name='error'),
    path('eliminar/<int:id>/', views.eliminarInventario, name='eliminar_inventario'),
    path('hospital/', views.listar_hospitales, name='listar_hospitales'),
    path('hospital/<int:id_hospital>/', views.detalles_inventario_hospital, name='detalles_inventario_hospital'),
]
