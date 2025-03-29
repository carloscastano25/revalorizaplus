from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario, Envase, CategoriaEnvase


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombre = forms.CharField(max_length=255)
    apellido = forms.CharField(max_length=255)
    cedula = forms.CharField(max_length=20, required=True)
    direccion = forms.CharField(max_length=255, required=False)
    telefono = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['nombre', 'apellido', 'cedula', 'direccion', 'telefono', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')  # Eliminar el campo username si está presente

        # Reordenar los campos
        self.fields['nombre'].widget.attrs.update({'placeholder': 'Nombre'})
        self.fields['apellido'].widget.attrs.update({'placeholder': 'Apellido'})
        self.fields['cedula'].widget.attrs.update({'placeholder': 'Cédula'})
        self.fields['direccion'].widget.attrs.update({'placeholder': 'Dirección'})
        self.fields['telefono'].widget.attrs.update({'placeholder': 'Teléfono'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmar Contraseña'})

        self.fields = {
            'nombre': self.fields['nombre'],
            'apellido': self.fields['apellido'],
            'cedula': self.fields['cedula'],
            'direccion': self.fields['direccion'],
            'telefono': self.fields['telefono'],
            'email': self.fields['email'],
            'password1': self.fields['password1'],
            'password2': self.fields['password2'],
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if User.objects.filter(username=cedula).exists():
            raise forms.ValidationError("La cédula ya está registrada.")
        return cedula

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['cedula']  # Usar la cédula como username
        if commit:
            user.save()
            perfil = PerfilUsuario(
                user=user,
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                cedula=self.cleaned_data['cedula'],
                direccion=self.cleaned_data['direccion'],
                telefono=self.cleaned_data['telefono'],
                rol='final'  # Asignar rol de usuario final
            )
            perfil.save()
        return user

class RegistroEnvaseForm(forms.Form):
    categoria = forms.ModelChoiceField(
        queryset=CategoriaEnvase.objects.all(),
        empty_label="Seleccione una categoría",
        label="Categoría de Envase"
    )

class BuscarUsuarioForm(forms.Form):
    cedula_usuario = forms.CharField(max_length=20, required=True)

