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
    def get(self, request, id=0, prov=None):
        if id > 0:
            recetas = list(Recetas.objects.filter(idreceta=id).values())
            if len(recetas) > 0:
                receta = recetas[0]
                datos = {"mensaje": "exito", "receta": recetas}
            else:
                datos = {"mensaje": "No se encontró la receta"}
        else:
            if prov:
                recetas = list(Recetas.objects.filter(idproveedor=prov).values())
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

    def put(self, request, id):
        pass