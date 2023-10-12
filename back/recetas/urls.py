from django.urls import path
from . import views
from .views import RecetaView

urlpatterns = [
    
    path('recetas/', RecetaView.as_view(), name="recetas_list"),
    path('recetas/<int:id>/', RecetaView.as_view(), name="recetas_process")
    
]