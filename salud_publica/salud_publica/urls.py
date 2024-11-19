from django.contrib import admin
from django.urls import path, include 
from django.contrib.auth.views import LoginView, LogoutView
from app import views
from django.urls import reverse_lazy



urlpatterns = [
    path('admin/', admin.site.urls),
    path('aumentar_salidas/<int:id_inventario>/', views.aumentar_salidas, name='aumentar_salidas'),
    path('redirect-admin/', views.redirect_to_admin, name='redirect_admin'),
    path('hospital/<int:id_hospital>/entrada/', views.entrada, name='entrada'),
    
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('error/<int:id_hospital>/', views.error, name='error'),
    path('eliminar/<int:id>/', views.eliminarInventario, name='eliminar_inventario'),
    path('hospital/', views.listar_hospitales, name='listar_hospitales'),
    path('hospital/<int:id_hospital>/', views.detalles_inventario_hospital, name='detalles_inventario_hospital'),
    path('redirect/', views.redirect_after_login, name='redirect_after_login'),
]
