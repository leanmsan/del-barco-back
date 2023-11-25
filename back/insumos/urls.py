from django.urls import path
from . import views
from .views import InsumoView
from .views import InformeInsumosView

urlpatterns = [
    path('insumos/', InsumoView.as_view(), name="insumos_list"),
    path('insumos/<int:id>/', InsumoView.as_view(), name="insumos_process"),
    path('informe_insumos/', InformeInsumosView.as_view(), name='informe_insumos')
]