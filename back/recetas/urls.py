from django.urls import path
from . import views
from .views import RecetaView, RecetadetalleView, GetLastIdRecetaView

urlpatterns = [
    
    path('recetas/', RecetaView.as_view(), name="recetas_list"),
    path('recetas/<int:id>/', RecetaView.as_view(), name="recetas_process"),
    path('receta_detalles/', RecetadetalleView.as_view(), name="recetadetalles_list"),
    path('receta_detalles/<int:id>/', RecetadetalleView.as_view(), name="recetadetalles_process"),
    path('recetaxprod/<int:prod>/', RecetadetalleView.as_view(), name="recetaxprod"),
    path('lastidreceta/', GetLastIdRecetaView.as_view(), name="getlastid"),
]