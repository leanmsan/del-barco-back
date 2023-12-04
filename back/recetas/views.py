from django.shortcuts import render
from common.models import (
    Receta,
    Recetadetalle,
    Insumo,
)

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
import json
from datetime import datetime

# VISTA DE RECETA

@method_decorator(csrf_exempt, name="dispatch")
class RecetaView(View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id=0):
        if id > 0:
            recetas = list(Receta.objects.filter(idreceta=id).values())
            if len(recetas) > 0:
                receta = recetas[0]
                datos = {"message": "exito", "receta": receta}
                return JsonResponse(datos, status=200)
            else:
                datos = {"message": "No se encontró la receta"}
                return JsonResponse(datos, status=404)
        else:
            recetas = list(Receta.objects.values())
            if len(recetas) > 0:
                datos = {
                    "message": "exito",
                    "cantidad": len(recetas),
                    "recetas": recetas,
                }
                return JsonResponse(datos, status=200)
            else:
                datos = {"message": "No se encontraron recetas"}
                return JsonResponse(datos, status=400)
    
    def post(self, request):
        jd = json.loads(request.body)
        nombre_receta = jd["nombre_receta"]
        
        if Receta.objects.filter(nombre_receta=nombre_receta).exists():
            datos = {'message': 'El nombre ya está en uso. No se creó la receta.'}
            return JsonResponse(datos, status=400)
        
        else:      
            recetas = Receta.objects.create(
                nombre_receta=nombre_receta,
                tipo=jd["tipo"],
                litros=jd["litros"]
            )
            last_inserted_receta = recetas.nombre_receta

            datos = {
                "message": "Se creó la receta con éxito",
                "last_inserted_receta": last_inserted_receta
            }
            return JsonResponse(datos, status=200)

    def patch(self, request, id):
        jd = json.loads(request.body)
        nombre_receta = jd.get('nombre_receta', None)

        try:
            receta = Receta.objects.get(idreceta=id)
        except Receta.DoesNotExist:
            datos = {'message': 'No se encontró la receta'}
            return JsonResponse(datos, status=400)

        if nombre_receta:
            recetas_mismo_nombre_receta = Receta.objects.filter(nombre_receta=nombre_receta)
            if recetas_mismo_nombre_receta.exists():
                datos = {'message': 'El nombre ya está en uso en otra receta. No se puede actualizar.'}
                return JsonResponse(datos, status=400)
            else:
                receta.nombre_receta=nombre_receta
        for field_name, field_value in jd.items():
            if field_name != 'proveedor_id' and hasattr(receta, field_name):
                setattr(receta, field_name, field_value)
        receta.save()
        datos = {'message': 'Receta actualizada'}
        return JsonResponse(datos, status=200)
    
@method_decorator(csrf_exempt, name="dispatch")
class GetLastIdRecetaView(View):
    #get para obtener el ultimo id
    def get(self, request):
        receta = Receta.objects.latest('idreceta')
        lastId = receta.idreceta
        lastIdReceta = {"message": "exito", "lastid": lastId}
        return JsonResponse(lastIdReceta)

# VISTA DE RECETA DETALLE

@method_decorator(csrf_exempt, name="dispatch")
class RecetadetalleView(View):

    def get(self, request, nombre_receta=0):
        if nombre_receta > 0:
            recetasdet = list(Recetadetalle.objects.filter(receta=nombre_receta).values())
            if len(recetasdet) > 0:
                datos = {"message": "exito", "recetas": recetasdet}
                return JsonResponse(datos, status=200)
            else:
                datos = {"message": "No se encontró el ID de receta"}
                return JsonResponse(datos, status=404)
        else:
            recetasdet = list(Recetadetalle.objects.values())
            if len(recetasdet) > 0:
                datos = {
                    "message": "exito",
                    "cantidad": len(recetasdet),
                    "recetas": recetasdet,
                }
                return JsonResponse(datos, status=200)
            else:
                datos = {"message": "No se encontraron detalles de receta"}
                return JsonResponse(datos, status=404)


    def post(self, request):
        jd = json.loads(request.body)
        receta_id = jd["receta_id"]
        insumo_id = jd["insumo_id"]
        cantidad = jd["cantidad"]
        cantidad = int(cantidad)

        try:
            receta = Receta.objects.get(nombre_receta=receta_id)
        except Receta.DoesNotExist:
            receta = None

        if receta:
            try:
                insumo = Insumo.objects.get(nombre_insumo=insumo_id)
            except Insumo.DoesNotExist:
                insumo = None

            if insumo:
                recetadetalle = Recetadetalle.objects.create(receta=receta, insumo=insumo, cantidad=cantidad, tipo_medida=jd["tipo_medida"])
                datos = {"message": "success"}
                return JsonResponse(datos, status=200)
            else:
                datos = {"message": "El insumo no existe"}
                return JsonResponse(datos, status=400)
        else:
            datos = {"message": "La receta no existe"}
            return JsonResponse(datos, status=400)



    def patch(self, request, id):
        jd = json.loads(request.body)
        try:
            recetadetalle = Recetadetalle.objects.get(idrecetadetalle=id)
        except Recetadetalle.DoesNotExist:
            datos = {'message': 'El detalle de receta no existe'}
            return JsonResponse(datos, status=404)
        insumo = jd.get('insumo', None)
        if insumo:
            if Insumo.objects.filter(nombre_insumo=insumo).none():
                datos = {'message': 'El insumo no existe. No se puede actualizar.'}
                return JsonResponse(datos, status=400)
            else:
                recetadetalle.insumo=jd["insumo_id"]
        for field_name, field_value in jd.items():
            if field_name != 'insumo_id' and hasattr(recetadetalle, field_name):
                setattr(recetadetalle, field_name, field_value)
        recetadetalle.save()
        datos = {'message': 'Receta actualizada'}
        return JsonResponse(datos, status=200)
        