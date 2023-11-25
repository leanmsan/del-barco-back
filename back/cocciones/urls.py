from django.urls import path
from . import views
from .views import CoccionView, InformeCoccionesView

urlpatterns = [
    path('cocciones/', CoccionView.as_view(), name="cocciones_list"),
    path('cocciones/<int:id>/', CoccionView.as_view(), name="cocciones_process"),
    path('informe_cocciones/', InformeCoccionesView.as_view(), name='informe_cocciones')
]