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
    nivel = Nivel.objects.filter(clases=clase)
    

    
    ctx = {
        #"form": ClaseForm(instance=clase),
        "clase": clase,
        "nivel": nivel[0],
    }
    
    if clase.id > 1:
        clasePrevia = clase.id - 1
        ctx["clasePrevia"] = clasePrevia
        
    if clase != nivel.last:
        clasePosterior = clase.id + 1
        ctx["clasePosterior"] = clasePosterior
        
    if request.POST:
        
        usuario = Usuario.objects.get(id=request.user.id)
        
        if request.POST.dict()["is_completed"] == 1:
            usuario.clases_vistas.add(clase)
            messages.info(request, "Completada 😄")
        else:
            usuario.clases_vistas.remove(clase)
            messages.info(request, "No completada 😔")
        
    return render(request, "aula/clase.html", ctx)
