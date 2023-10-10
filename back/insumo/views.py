from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from common.models import Insumo, Proveedor
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
import json

# Create your views here.

class InsumoView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id=0):
        if id > 0:
            insumos = list(Insumo.objects.filter(idinsumo=id).values())
            if len(insumos) > 0:
                insumo = insumos[0]
                datos = {'mensaje': 'exito', 'insumo': insumo}
            else:
                datos = {'mensaje': 'No se encontró el insumo'}
            return JsonResponse(datos)
        else:
            insumos = list(Insumo.objects.values())
            if len(insumos) > 0:
                datos = {'mensaje': 'exito', 'cantidad': len(insumos), 'insumos': insumos}
            else:
                datos = {'mensaje': 'No se encontraron insumos'}
        return JsonResponse(datos)
    
    def post(self, request):
        jd = json.loads(request.body)
        proveedor_id=jd['proveedor_id']
        try:
            prov = Proveedor.objects.get(nombre=proveedor_id)
        except Proveedor.DoesNotExist:
            prov = None
        if prov:
            insumo = Insumo.objects.create(descripcion=jd['descripcion'], precio_unitario=jd['precio_unitario'], cantidad_disponible=jd['cantidad_disponible'], tipo_medida=jd['tipo_medida'], categoria=jd['categoria'], proveedor=prov)
            datos = {'mensaje': 'success'}
        else:
            datos = {'mensaje': 'El rubro no existe'}
        return JsonResponse(datos)


    def patch(self, request, id):
        jd = json.loads(request.body)
        insumos = list(Insumo.objects.filter(idinsumo=id).values())
        if len(insumos) > 0:
            insumo = Insumo.objects.get(idinsumo=id)
            insumo.descripcion = jd['descripcion']
            insumo.cantidad_disponible = jd['cantidad_disponible']
            insumo.tipo_medida = jd['tipo_medida']
            insumo.categoria = jd['categoria']
            insumo.precio_unitario = jd['precio_unitario']
            insumo.save()
            datos = {'mensaje': 'Insumo actualizado correctamente'}
        else:
            datos = {'mensaje': 'No se encontró el insumo'}
        return JsonResponse(datos)