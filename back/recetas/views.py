from django.shortcuts import render
from common.models import (
    Recetas,
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
    def get(self, request, id=0):
        if id > 0:
            recetas = list(Recetas.objects.filter(idreceta=id).values())
            if len(recetas) > 0:
                receta = recetas[0]
                datos = {"mensaje": "exito", "recetas": recetas}
            else:
                datos = {"mensaje": "No se encontró la receta solicitada"}
        else:
            recetas = list(Recetas.objects.values())
            if len(recetas) > 0:
                datos = {
                    "mensaje": "exito",
                    "cantidad": len(recetas),
                    "recetas": recetas,
                }
            else:
                datos = {"mensaje": "No se encontraron recetas"}

        return JsonResponse(datos)
    
    def post(self, request):
        jd = json.loads(request.body)
        nombre = jd["nombre"]
        
        if Recetas.objects.filter(nombre=nombre).exists():
            datos = {'message': 'El nombre ya está en uso. No se creó la receta.'}
            return JsonResponse(datos, status=400)
        
        else:      
            recetas = Recetas.objects.create(
                nombre=nombre,
                tipo=jd["tipo"],
                fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            last_inserted_id = recetas.idreceta

            datos = {
                "mensaje": "Se creó la receta con éxito",
                "last_inserted_id": last_inserted_id,
            }

        return JsonResponse(datos)

    def patch(self, request, id):
        jd = json.loads(request.body)
        nombre = jd.get('nombre', None)

        if nombre:
            recetas_mismo_nombre = Insumo.objects.filter(nombre=nombre).exclude(idreceta=id)

            if recetas_mismo_nombre.exists():
                datos = {'mensaje': 'El nombre ya está en uso en otra receta. No se puede actualizar.'}
                return JsonResponse(datos, status=400)

        try:
            receta = Recetas.objects.get(idreceta=id)
        except Recetas.DoesNotExist:
            datos = {'mensaje': 'No se encontró la receta'}
            return JsonResponse(datos, status=404)

        for field_name, field_value in jd.items():
            if hasattr(receta, field_name):
                setattr(receta, field_name, field_value)

        receta.save()

        datos = {'mensaje': 'Receta actualizada'}
        return JsonResponse(datos)

# VISTA DE RECETA DETALLE


@method_decorator(csrf_exempt, name="dispatch")
class RecetadetalleView(View):

    def get(self, request, id=0, insumo=0):
        if id > 0:
            recetasdet = list(Recetadetalle.objects.filter(idreceta=id).values())
            if len(recetasdet) > 0:
                datos = {"mensaje": "exito", "recetas": recetasdet}
            else:
                datos = {"mensaje": "No se encontró el ID de receta"}
        else:
            if insumo:
                recetasdet = list(
                    Recetadetalle.objects.filter(idinsumo=insumo).values()
                )
            else:
                recetasdet = list(Recetadetalle.objects.values())

            if len(recetasdet) > 0:
                datos = {
                    "mensaje": "exito",
                    "cantidad": len(recetasdet),
                    "recetas": recetasdet,
                }
            else:
                datos = {"mensaje": "No se encontraron detalles de receta"}

        return JsonResponse(datos)


    def post(self, request):
        jd = json.loads(request.body)
        idreceta_id = jd["idreceta_id"]
        idinsumo_id = jd["idinsumo_id"]
        cantidad = jd["cantidad"]
        cantidad = int(cantidad)

        try:
            receta = Recetas.objects.get(idreceta=idreceta_id)
        except Recetas.DoesNotExist:
            receta = None

        if receta:
            try:
                insumo = Insumo.objects.get(idinsumo=idinsumo_id)
            except Insumo.DoesNotExist:
                insumo = None

            if insumo:
                recetadetalle = Recetadetalle.objects.create(
                    idreceta=receta,
                    idinsumo=insumo,
                    cantidad=cantidad,
                    tipomedida=jd["tipomedida"],
                    )
                datos = {"mensaje": "success"}
            else:
                datos = {"mensaje": "El insumo no existe"}
        else:
            datos = {"mensaje": "La receta no existe"}
        return JsonResponse(datos)


    def patch(self, request, detalle_id):
        jd = json.loads(request.body)

        try:
            receta_detalle = Recetadetalle.objects.get(id=detalle_id)
        except Recetadetalle.DoesNotExist:
            datos = {'mensaje': 'El detalle de receta no existe'}
            return JsonResponse(datos, status=404)

        if 'idreceta' in jd:
            idreceta = jd['idreceta']
            try:
                receta = Recetas.objects.get(idreceta=idreceta)
            except Recetas.DoesNotExist:
                datos = {'mensaje': 'La receta especificada no existe'}
                return JsonResponse(datos, status=404)

        for field_name, field_value in jd.items():
                if hasattr(receta_detalle, field_name):
                    setattr(receta_detalle, field_name, field_value)

        receta_detalle.save()

        datos = {'mensaje': 'Detalle de receta actualizado correctamente'}
        return JsonResponse(datos)