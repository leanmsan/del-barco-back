from django.urls import path
from . import views
from .views import CoccionView

urlpatterns = [
    path('cocciones/', CoccionView.as_view(), name="cocciones_list"),
    path('cocciones/<int:id>/', CoccionView.as_view(), name="cocciones_process"),

]