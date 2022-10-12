from django.urls import path
from . import views

urlpatterns = [
    #2 LOGIN URLS
    path('registro/', views.registro, name="registro"),
    
    #2 INICIO
    path('', views.inicio, name="inicio"),
    
    #2 OPCIONES
    path('opciones/', views.opciones, name="opciones"),
    
    #2 AULAS URLS
    path('clase/<id>/', views.clase, name="clase"),
]