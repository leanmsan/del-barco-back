
from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from common.models import Coccion, Receta, Insumo, Recetadetalle
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
import json
from datetime import datetime

class CoccionView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, receta=0):
        if receta > 0:
            cocciones = list(Coccion.objects.filter(receta=receta).values())
            if len(cocciones) > 0:
                coccion = cocciones[0]
                datos = {'message': 'exito', 'coccion': coccion}
                return JsonResponse(datos, status=200)
            else:
                datos = {'message': 'No se encontró la coccion'}
                return JsonResponse(datos, status=404)
        else:
            cocciones = list(Coccion.objects.values())
            if len(cocciones) > 0:
                datos = {'message': 'exito', 'cantidad': len(cocciones), 'cocciones': cocciones}
                return JsonResponse(datos, status=200)
            else:
                datos = {'message': 'No se encontraron cocciones'}
                return JsonResponse(datos, status=404)
            
    def post(self, request):
        jd = json.loads(request.body)
        receta_id = jd['receta_id']
        insuficientes = list()
        fecha = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        listainsumos = list()
        cantdis = list()
        try:
            receta = Receta.objects.get(nombre_receta=receta_id)
            print(f'Esto es receta {receta}')
        except Receta.DoesNotExist:
            receta = None

        if receta:
            recetadetalle = Recetadetalle.objects.filter(receta=receta_id)
            for detalle in recetadetalle:
                listainsumos.append(detalle.insumo)
                print(f'esto es lista insumo {listainsumos}')
                insumo_disponible = Insumo.objects.filter(nombre_insumo = detalle.insumo)
                print(f'esto es insumo disponible {insumo_disponible}')
                #cantdis.append()
                print(f'Esto es cantidad disponible {cantdis}')
                for insumo in listainsumos:
                    if detalle.cantidad > Insumo.objects.get(detalle.cantidad_disponible):
                        insuficientes.append(insumo.nombre_insumo)

            if insuficientes:
                return JsonResponse({'message': f'No hay suficiente stock de {", ".join(insuficientes)}'})
            else:
                for insumo in listainsumos:
                    print(f'Restando {detalle.cantidad} a {insumo.nombre}')
                    insumo.cantidad_disponible -= detalle.cantidad
                    insumo.save()
                coccion = Coccion.objects.create(receta=receta, volumen_producido=jd['volumen_producido'], fecha_coccion=fecha)
                datos = {'message': 'Coccion creada correctamente'}
                return JsonResponse(datos, status=200)
        else:
            datos = {'message': 'La receta no existe'}
            return JsonResponse(datos, status=400)