from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

urlpatterns = [
    # Administración
    path('admin/', admin.site.urls),

    # Usuarios
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('buscar_usuario/', views.buscar_usuario, name='buscar_usuario'),

    # Registro
    path('registro/', views.registro, name='registro'),

    # Inicio de Sesión
    path('login/', CustomLoginView.as_view(), name='login'),

    # Cierre de Sesión
    path('logout/', auth_views.LogoutView.as_view(next_page='pagina_principal'), name='logout'),

    # Perfil de Usuario
    path('perfil_usuario/<int:usuario_id>/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/', views.perfil_usuario_actual, name='perfil_usuario_actual'),

    # Registrar Envases
    path('registrar_envase/<int:usuario_id>/', views.registrar_envases, name='registrar_envase'),

    # Página Principal
    path('', views.pagina_principal, name='pagina_principal'),
]