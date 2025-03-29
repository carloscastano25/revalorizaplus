from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('final', 'Usuario Final'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    cedula = models.CharField(max_length=20, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='final')  # Rol por defecto

    def __str__(self):
        return f"{self.nombre} {self.apellido} - Cédula: {self.cedula}"
    
    def es_administrador(self):
        return self.rol == 'admin'

    def es_usuario_final(self):
        return self.rol == 'final'

class CategoriaEnvase(models.Model):
    nombre_categoria = models.CharField(max_length=255)
    ml_minimo = models.IntegerField()
    ml_maximo = models.IntegerField(null=True, blank=True)  # Puede ser NULL para categorías sin límite superior
    puntos_asignados = models.IntegerField()

    def __str__(self):
        if self.ml_maximo:
            return f"{self.nombre_categoria}: desde {self.ml_minimo} ml hasta {self.ml_maximo} ml"
        else:
            return f"{self.nombre_categoria}: desde {self.ml_minimo} ml en adelante"

class Supermercado(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    horario = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Envase(models.Model):
    tamaño = models.IntegerField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaEnvase, on_delete=models.CASCADE)

    def __str__(self):
        return f"Envase de {self.tamaño}ml registrado por {self.usuario}"

class Punto(models.Model):
    cantidad = models.IntegerField()
    fecha_otorgamiento = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cantidad} puntos otorgados a {self.usuario.nombre} {self.usuario.apellido} - Cédula: {self.usuario.cedula} el {self.fecha_otorgamiento}"

class Bono(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_emision = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    supermercado = models.ForeignKey(Supermercado, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bono de ${self.valor} para {self.supermercado} (Usuario: {self.usuario})"

class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('ganancia', 'Ganancia'),
        ('canje', 'Canje'),
    ]
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    cantidad_puntos = models.IntegerField()
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    puntos = models.ManyToManyField(Punto) # Relación muchos a muchos con Punto

    def __str__(self):
        return f"{self.tipo} de {self.cantidad_puntos} puntos por {self.usuario} el {self.fecha_transaccion}"