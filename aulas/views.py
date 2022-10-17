from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Usuario, Nivel, Clase
from .forms import ClaseForm, CustomCreationForm

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
    INICIO
"""
@login_required(redirect_field_name='')
def inicio(request):
    usuario = request.user
    messages.info(request, f"Ultima conexción: {usuario.last_login.strftime('%a %d de %m, a las %H:%M')}")
        
    return render(request, "index.html")

@login_required(redirect_field_name='')
def opciones(request):
    
    if request.method == "POST":
        value = request.POST['tema'] 
        Usuario.objects.filter(id=request.user.id).update(tema=value)
        return redirect(to="opciones")
    
    return render(request, "opciones.html")

"""
    AULA
"""

@login_required(redirect_field_name='')
def clase(request, slug, id):
    clase = get_object_or_404(Clase, id=id)   
    nivel = get_object_or_404(Nivel, slug=slug)    
    ctx = {
        "clase": clase,
        "nivel": nivel,
    }
    
    clases = Clase.objects.filter(nivel=nivel)
    pks = []
    for c in clases:
        pks.append(c.pk)
    
    if pks.index(clase.id) != 0:
        clase_pre = pks.index(clase.id) - 1 
        ctx["clase_pre"] = pks[clase_pre]
        
    if pks.index(clase.id) != len(pks) - 1:
        clase_pos = pks.index(clase.id) + 1
        ctx["clase_pos"] = pks[clase_pos]
    
        
    if request.POST:
        
        usuario = Usuario.objects.get(id=request.user.id)
        
        if request.POST.dict()["is_completed"] == "yes":
            usuario.clases_vistas.add(clase)
            messages.info(request, "Completada 😄")
        else:
            usuario.clases_vistas.remove(clase)
            messages.info(request, "No completada 😔")
        
    return render(request, "aula/clase.html", ctx)
