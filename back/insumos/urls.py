from django.urls import path
from . import views
from .views import InsumoView

urlpatterns = [
    path('insumos/', InsumoView.as_view(), name="insumos_list"),
    path('insumos/<int:id>/', InsumoView.as_view(), name="insumos_process"),

]