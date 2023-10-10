from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from common.models import Proveedor
from django.views import View
from django.http.response import JsonResponse, HttpResponse
import json

# Create your views here.

class ProveedorView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,id=0):
        if id > 0:
            proveedores = list(Proveedor.objects.filter(idproveedor=id).values())
            if len(proveedores) > 0:
                proveedor = proveedores[0]
                datos = {'mensaje': 'exito', 'proveedor': proveedor}    
            else:
                datos = {'mensaje': 'no se encuentra proveedores'}
            return JsonResponse(datos)
        else:
            proveedores = list(Proveedor.objects.values())
            if len(proveedores) > 0:
                datos = {'mensaje': 'exito', 'proveedores': proveedores}
            else:
                datos = {'mensaje': 'no se encuentran proveedores'}
            return JsonResponse(datos)

    def post(self,request):
        jd = json.loads(request.body)
        nombre= jd['nombre']
        if Proveedor.objects.filter(nombre=nombre).exists():
            datos = {'mensaje': 'Proveedor ya existente'}
            return JsonResponse(datos, status=400)
        else:
            Proveedor.objects.create(nombre= jd['nombre'], mail = jd['mail'], telefono = jd['telefono'], estado = jd['estado'])
            datos = {'mensaje': 'success'}
        return JsonResponse(datos, status=201)

    def put(self,request,id):
        jd = json.loads(request.body)
        proveedores = list(Proveedor.objects.filter(idproveedor=id).values())
        if len(proveedores) > 0:
            proveedor = Proveedor.objects.get(idproveedor=id)
            proveedor.nombre = jd['nombre']
            proveedor.mail = jd['mail']
            proveedor.telefono = jd['telefono']
            proveedor.estado = jd['estado']
            proveedor.save()
            datos = {'mensaje': 'Proveedor actualizado correctamente'}
        else:
            datos = {'mensaje': 'No se encontro el proveedor'}
        return JsonResponse(datos)