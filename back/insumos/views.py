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
                return JsonResponse(datos, status=200)
            else:
                datos = {'message': 'No se encontró el insumo'}
                return JsonResponse(datos, status=404)
        else:
            insumos = list(Insumo.objects.values())
            if len(insumos) > 0:
                datos = {'message': 'exito', 'cantidad': len(insumos), 'insumos': insumos}
                return JsonResponse(datos, status=200)
            else:
                datos = {'message': 'No se encontraron insumos'}
                return JsonResponse(datos, status=404)
    
    def post(self, request):
        jd = json.loads(request.body)
        nombre_insumo = jd['nombre_insumo']
        
        if Insumo.objects.filter(nombre_insumo=nombre_insumo).exists():
            datos = {'message': 'Este nombre ya existe. No se puede crear el insumo.'}
            return JsonResponse(datos, status=400)

        proveedor_id = jd['proveedor_id']
        try:
            proveedor = Proveedor.objects.get(nombre_proveedor=proveedor_id)
        except Proveedor.DoesNotExist:
            proveedor = None

        if proveedor:

            insumo = Insumo.objects.create(nombre_insumo=nombre_insumo, precio_unitario=jd['precio_unitario'], cantidad_disponible=jd['cantidad_disponible'], tipo_medida=jd['tipo_medida'], categoria=jd['categoria'], proveedor=proveedor)
            datos = {'message': 'Insumo creado correctamente'}
            return JsonResponse(datos, status=200)
        else:
            datos = {'message': 'El proveedor no existe'}
            return JsonResponse(datos, status=400)


    def patch(self, request, id):
        jd = json.loads(request.body)
        nombre_insumo = jd.get('nombre_insumo', None)

        if nombre_insumo:
            insumos_con_mismo_nombre = Insumo.objects.filter(nombre_insumo=nombre_insumo).exclude(idinsumo=id)

            if insumos_con_mismo_nombre.exists():
                datos = {'message': 'El nombre ya existe en otro insumo. No se puede actualizar.'}
                return JsonResponse(datos, status=400)

        try:
            insumo = Insumo.objects.get(idinsumo=id)
        except Insumo.DoesNotExist:
            datos = {'message': 'No se encontró el insumo'}
            return JsonResponse(datos, status=404)
        proveedor_id = jd['proveedor_id']
        
        if proveedor_id:
            if Proveedor.objects.get(nombre_proveedor=proveedor_id):
                a = 2 + 2
            else:
                datos = {'message': 'El proveedor proporcionado no existe'}
                return JsonResponse(datos, status=404)
            
        for field_name, field_value in jd.items():
            if hasattr(insumo, field_name):
                setattr(insumo, field_name, field_value)

        insumo.save()

        datos = {'message': 'Insumo actualizado correctamente'}
        return JsonResponse(datos, status= 200)