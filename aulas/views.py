from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Usuario, Nivel, Clase
from .forms import ClaseForm, CustomCreationForm

"""
    INICIO
"""
@login_required(redirect_field_name='')
def inicio(request):            
    return render(request, "index.html")

"""
    AUTENTICACIÓN
"""
@login_required(redirect_field_name='')    
def registro(request):
    if request.user.is_admin:
        ctx = {
            "form": CustomCreationForm()
        }
        return render(request, "registration/registro.html", ctx)
    else:
        return redirect(to="inicio")

"""
    AULA
"""

@login_required(redirect_field_name='')
def clase(request, id):
    clase = get_object_or_404(Clase, id=id)
    
    ctx = {
        "form": ClaseForm(instance=clase),
        "clase": clase
    }
    
    if request.method == "POST":
        data = ClaseForm(data=request.POST, instance=clase)
        if data.is_valid():
            data.save()
            messages.info(request, "Clase editada correctamente")
            return redirect(to="clase")
        else:
            ctx["form"] = data
        
    return render(request, "aula/clase.html", ctx)
