from django.urls import path
from . import views
from .views import ProveedorView

urlpatterns = [
    
    path('proveedores/', ProveedorView.as_view(), name="proveedores_list"),
    path('proveedores/<int:id>/', ProveedorView.as_view(), name="proveedores_process")
    
]