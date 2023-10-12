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
                datos = {'message': 'exito', 'insumo': insumo}
            else:
                datos = {'message': 'No se encontró el insumo'}
            return JsonResponse(datos)
        else:
            insumos = list(Insumo.objects.values())
            if len(insumos) > 0:
                datos = {'message': 'exito', 'cantidad': len(insumos), 'insumos': insumos}
            else:
                datos = {'message': 'No se encontraron insumos'}
        return JsonResponse(datos)
    
    def post(self, request):
        jd = json.loads(request.body)
        descripcion = jd['descripcion']
        
        if Insumo.objects.filter(descripcion=descripcion).exists():
            datos = {'message': 'La descripción ya existe. No se puede crear el insumo.'}
            return JsonResponse(datos, status=400)
        
        proveedor_id = jd['proveedor_id']
        try:
            prov = Proveedor.objects.get(nombre=proveedor_id)
        except Proveedor.DoesNotExist:
            prov = None

        if prov:
            insumo = Insumo.objects.create(descripcion=descripcion, precio_unitario=jd['precio_unitario'], cantidad_disponible=jd['cantidad_disponible'], tipo_medida=jd['tipo_medida'], categoria=jd['categoria'], proveedor=prov)
            datos = {'message': 'Insumo creado correctamente'}
        else:
            datos = {'message': 'El proveedor no existe'}
        
        return JsonResponse(datos)


    def patch(self, request, id):
        jd = json.loads(request.body)
        descripcion = jd.get('descripcion', None)

        if descripcion:
            insumos_con_misma_descripcion = Insumo.objects.filter(descripcion=descripcion).exclude(idinsumo=id)

            if insumos_con_misma_descripcion.exists():
                datos = {'mensaje': 'La descripción ya existe en otro insumo. No se puede actualizar.'}
                return JsonResponse(datos, status=400)

        try:
            insumo = Insumo.objects.get(idinsumo=id)
        except Insumo.DoesNotExist:
            datos = {'mensaje': 'No se encontró el insumo'}
            return JsonResponse(datos, status=404)

        for field_name, field_value in jd.items():
            if hasattr(insumo, field_name):
                setattr(insumo, field_name, field_value)

        insumo.save()

        datos = {'mensaje': 'Insumo actualizado correctamente'}
        return JsonResponse(datos)