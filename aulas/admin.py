from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Usuario, Nivel, Clase
from .forms import NivelForm, ClaseForm
# Register your models here.

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('username', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username','email','is_admin')
    list_editable = ('is_admin',)
    list_filter = ('is_admin',)
    fieldsets = (
        ('Datos de Acceso', {'fields': ('username','password','is_superuser')}),
        ('Información Personal', {'fields': (
            'first_name',
            'last_name',
            'telefono',
            'email',
            'tema',
        )}),
        ('Aula', {'fields': ('niveles','clases_vistas')}),
        ('Permisos', {'fields': ('is_admin','is_maestro','is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ['username']
    search_help_text = 'Busqueda por usuario'    
    ordering = ('username',)
    filter_horizontal = ('niveles', 'clases_vistas')

class NivelAdmin(admin.ModelAdmin):    
    list_display = ('nombre', 'slug')
    list_display_links = ('nombre',)    
    fieldsets = (
        ('Información general',
            {
                'fields': (
                    'nombre',
                ),
                'description': '<p style="margin:20px 0;">Datos sobre el Nivel</p>'
            }
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre'),
        }),
    )
    search_fields = ['nombre']
    search_help_text = 'Busqueda por nombre'

class ClaseAdmin(admin.ModelAdmin):
    form = ClaseForm
    
    list_display = ('titulo', 'nivel', 'is_available')
    list_display_links = ('titulo',)
    list_editable = ('nivel','is_available')
    
    fieldsets = (
        ('Información general',
            {
                'fields': (
                    'titulo',
                    'nivel',
                    'is_available',
                    'p_general',
                    'p_especifico',
                ),
                'description': '<p style="margin:20px 0;">Información sobre la clase</p>'
            }
        ),
        ('Archivos', {'fields': ('video', 'material')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('titulo', 'p_general', 'p_espeficico', 'video', 'material','is_available'),
        }),
    )
    radio_fields = {'is_available': admin.HORIZONTAL}
    
    search_fields = ['titulo']
    search_help_text = 'Busqueda por título'
    

admin.site.register(Usuario, UserAdmin)
admin.site.register(Nivel, NivelAdmin)
admin.site.register(Clase, ClaseAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)