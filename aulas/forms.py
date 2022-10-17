from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Nivel, Clase

class CustomCreationForm(UserCreationForm):
    
    class Meta:
        model = Usuario
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'telefono',
            'niveles']
        
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

class NivelForm(forms.ModelForm):
    
    class Meta:
        model = Nivel
        fields = '__all__'
        
class ClaseForm(forms.ModelForm):
    
    class Meta:
        model = Clase
        fields = '__all__'
        
        widgets = {
            'material': forms.ClearableFileInput(attrs={'multiple': True, 'required': False}),
        }
        
