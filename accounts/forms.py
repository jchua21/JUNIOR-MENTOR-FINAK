from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Nombre de Usuario",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese su nombre de usuario'}),
                               help_text="<small>Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_.</small>")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Ingrese su dirección de correo electrónico'}))
    first_name = forms.CharField(label="Nombre",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Nombre'}))
    last_name = forms.CharField(label="Apellido",widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Ingrese su Apellido'}))
    password1 = forms.CharField(label="Contraseña",widget=forms.PasswordInput(attrs={'class':'form-control'}),
                                help_text="<small><ul><li>Su contraseña no puede ser demasiado similar a su otra información personal.</li>\
                                        <li>Su contraseña debe contener al menos 8 caracteres.</li>\
                                        <li>Su contraseña no puede ser una contraseña comúnmente utilizada.</li>\
                                        <li>Su contraseña no puede ser completamente numérica.</li></ul></small>")
    password2 = forms.CharField(label="Confirmación de contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}),\
            help_text="<small>Ingrese la misma contraseña que antes, para verificación.</small>")
    class Meta:
        model = User
        fields=['username','email','first_name','last_name','password1', 'password2',]

