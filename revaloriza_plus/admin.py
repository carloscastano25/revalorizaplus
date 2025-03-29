from django.contrib import admin
from .models import PerfilUsuario, CategoriaEnvase, Supermercado, Envase, Punto, Bono, Transaccion

admin.site.register(PerfilUsuario)
admin.site.register(CategoriaEnvase)
admin.site.register(Supermercado)
admin.site.register(Envase)
admin.site.register(Punto)
admin.site.register(Bono)
admin.site.register(Transaccion)