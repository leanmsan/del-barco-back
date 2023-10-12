from django.urls import path
from . import views
from .views import ProveedorView

urlpatterns = [
    
    path('recetas/', ProveedorView.as_view(), name="recetas_list"),
    path('recetas/<int:id>/', ProveedorView.as_view(), name="recetas_process")
    
]