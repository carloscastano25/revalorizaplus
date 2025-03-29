from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('buscar_usuario/', views.buscar_usuario, name='buscar_usuario'),
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),    
    path('perfil_usuario/<int:usuario_id>/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/', views.perfil_usuario_actual, name='perfil_usuario_actual'),  # Nueva ruta
    path('registrar_envase/<int:usuario_id>/', views.registrar_envases, name='registrar_envase'),
    path('', views.pagina_principal, name='pagina_principal'),  
]