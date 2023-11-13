
from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from common.models import Proveedor
from django.views import View
from django.http.response import JsonResponse, HttpResponse
import json

class ProveedorView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self,request,id=0):
        if id > 0:
            proveedores = list(Proveedor.objects.filter(idproveedor=id).values())
            if len(proveedores) > 0:
                proveedor = proveedores[0]
                datos = {'message': 'exito', 'proveedor': proveedor}    
            else:
                datos = {'message': 'no se encuentra proveedores'}
            return JsonResponse(datos)
        else:
            proveedores = list(Proveedor.objects.values())
            if len(proveedores) > 0:
                datos = {'message': 'exito', 'proveedores': proveedores}
            else:
                datos = {'message': 'no se encuentran proveedores'}
            return JsonResponse(datos)

    def post(self,request):
        jd = json.loads(request.body)
        nombre_proveedor= jd['nombre_proveedor']
        if Proveedor.objects.filter(nombre_proveedor=nombre_proveedor).exists():
            datos = {'message': 'Proveedor ya existente'}
            return JsonResponse(datos, status=400)
        else:
            if len(nombre_proveedor) < 3:
                datos = {'message': 'Nombre inválido'}
                return JsonResponse(datos, status=400)
            else:
                Proveedor.objects.create(nombre_proveedor= jd['nombre_proveedor'], mail = jd['mail'], telefono = jd['telefono'], estado = 'A')
                datos = {'message': 'success'}
                return JsonResponse(datos, status=201)

    def patch(self,request,id):
        jd = json.loads(request.body)
        nombre_proveedor = jd.get('nombre_proveedor', None)

        if nombre_proveedor:
            proveedor_con_mismo_nombre = Proveedor.objects.filter(nombre_proveedor=nombre_proveedor).exclude(idproveedor=id)

            if proveedor_con_mismo_nombre.exists():
                datos = {'message': 'El nombre ya existe en otro proveedor. No se puede actualizar.'}
                return JsonResponse(datos, status=400)

        try:
            proveedor = Proveedor.objects.get(idproveedor=id)
        except Proveedor.DoesNotExist:
            datos = {'message': 'No se encontró el proveedor'}
            return JsonResponse(datos, status=404)

        for field_name, field_value in jd.items():
            if hasattr(proveedor, field_name):
                setattr(proveedor, field_name, field_value)

        proveedor.save()

        datos = {'message': 'Proveedor actualizado correctamente'}
        return JsonResponse(datos)