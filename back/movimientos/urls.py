from django.urls import path
from . import views
from .views import *

urlpatterns = [

    path('entradas/', EntradaView.as_view(), name="entradas_list"),
    path('entradas/<int:id>/', EntradaView.as_view(), name="entradas_process"),
    path('entradasxprov/<int:prov>/', EntradaView.as_view(), name="entradasxprov"),

    path('lastidentrada/', GetLastIdEntradaView.as_view(), name="getlastid"),
    path('lastidsalida/', GetLastIdSalidaView.as_view(), name="getlastid"),

    path('entrada_detalles/', EntradadetalleView.as_view(), name="entradadetalles_list"),
    path('entrada_detalles/<int:id>/', EntradadetalleView.as_view(), name="entradadetalles_process"),
    path('entradasxprod/<int:prod>/', EntradadetalleView.as_view(), name="entradasxprod"),
    
    path('salidas/', SalidaView.as_view(), name="salidas_list"),
    path('salidas/<int:id>/', SalidaView.as_view(), name="salidas_process"),
    path('salidasxprov/<int:prov>/', SalidaView.as_view(), name="salidasxprov"),
    
    path('salida_detalles/', SalidadetalleView.as_view(), name="salidadetalles_list"),
    path('salida_detalles/<int:id>/', SalidadetalleView.as_view(), name="salidadetalles_process"),
    path('salidasxprod/<int:prod>/', SalidadetalleView.as_view(), name="salidasxprod") 
]
