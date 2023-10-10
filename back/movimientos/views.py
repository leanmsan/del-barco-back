from django.shortcuts import render
from common.models import (
    Entrada,
    Entradadetalle,
    Salida,
    Salidadetalle,
    Proveedor,
    Insumo,
)

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
import json
from datetime import datetime


# VISTA DE ENTRADA

@method_decorator(csrf_exempt, name="dispatch")
class EntradaView(View):
    def get(self, request, id=0, prov=None):
        if id > 0:
            entradas = list(Entrada.objects.filter(identrada=id).values())
            if len(entradas) > 0:
                entrada = entradas[0]
                datos = {"mensaje": "exito", "entrada": entrada}
            else:
                datos = {"mensaje": "No se encontró el movimiento de entrada"}
        else:
            if prov:
                entradas = list(Entrada.objects.filter(idproveedor=prov).values())
            else:
                entradas = list(Entrada.objects.values())

            if len(entradas) > 0:
                datos = {
                    "mensaje": "exito",
                    "cantidad": len(entradas),
                    "entradas": entradas,
                }
            else:
                datos = {"mensaje": "No se encontraron movimientos de entrada"}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        idproveedor_id = jd["idproveedor_id"]

        try:
            idproveedor = Proveedor.objects.get(idproveedor=idproveedor_id)
        except Proveedor.DoesNotExist:
            idproveedor = None

        if idproveedor:
            entrada = Entrada.objects.create(
                idproveedor=idproveedor,
                fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                montototal=jd["montototal"],
            )
            last_inserted_id = entrada.identrada

            datos = {
                "mensaje": "success",
                "last_inserted_id": last_inserted_id,
            }
        else:
            datos = {"mensaje": "El proveedor no existe"}

        return JsonResponse(datos)

    def put(self, request, id):
        pass


# VISTA DE ENTRADA DETALLE

@method_decorator(csrf_exempt, name="dispatch")
class EntradadetalleView(View):
    def get(self, request, id=0, insumo=0):
        if id > 0:
            entradasdet = list(Entradadetalle.objects.filter(identrada=id).values())
            if len(entradasdet):
                datos = {"mensaje": "exito", "entradas": entradasdet}
            else:
                datos = {"mensaje": "No se encontró el id de entrada"}
            return JsonResponse(datos)
        else:
            if insumo:
                entradasdet = list(
                    Entradadetalle.objects.filter(idInsumo=insumo).values()
                )
            else:
                entradasdet = list(Entradadetalle.objects.values())

            if len(entradasdet) > 0:
                datos = {
                    "mensaje": "exito",
                    "cantidad": len(entradasdet),
                    "entradas": entradasdet,
                }
            else:
                datos = {"mensaje": "No se encontraron detalles de entrada"}
            return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        identrada_id = jd["identrada_id"]
        idinsumo_id = jd["idinsumo_id"]

        try:
            identrada = Entrada.objects.get(identrada=int(identrada_id))
        except Entrada.DoesNotExist:
            identrada = None

        if identrada:
            try:
                idinsumo = Insumo.objects.get(idinsumo=idinsumo_id)
            except Insumo.DoesNotExist:
                idInsumo = None

            if idinsumo:
                entrada = Entradadetalle.objects.create(
                    identrada=identrada,
                    idInsumo=idinsumo,
                    cantidad=jd["cantidad"],
                    preciounitario=jd["preciounitario"],
                )
                datos = {"mensaje": "success"}
            else:
                datos = {"mensaje": "El insumo no existe"}
        else:
            datos = {"mensaje": "La entrada no existe"}

        return JsonResponse(datos)

    def put(self, request, id):
        pass


# VISTA DE SALIDA


@method_decorator(csrf_exempt, name="dispatch")
class SalidaView(View):
    def get(self, request, id=0, prov=None):
        if id > 0:
            salidas = list(Salida.objects.filter(idsalida=id).values())
            if len(salidas) > 0:
                salida = salidas[0]
                datos = {"mensaje": "exito", "salida": salida}
            else:
                datos = {"mensaje": "No se encontró el movimiento de salida"}
        else:
            if prov:
                salidas = list(Salida.objects.filter(idproveedor=prov).values())
            else:
                salidas = list(Salida.objects.values())

            if len(salidas) > 0:
                datos = {
                    "mensaje": "exito",
                    "cantidad": len(salidas),
                    "salidas": salidas,
                }
            else:
                datos = {"mensaje": "No se encontraron movimientos de salida"}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        idproveedor_id = jd["idproveedor_id"]
        try:
            idproveedor = Proveedor.objects.get(idproveedor=idproveedor_id)
        except Proveedor.DoesNotExist:
            idproveedor = None

        if idproveedor:
            entrada = Entrada.objects.create(
                idproveedor=idproveedor,
                fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                montototal=jd["montototal"],
            )
            last_inserted_id = entrada.identrada

            datos = {
                "mensaje": "success",
                "last_inserted_id": last_inserted_id,
            }
        else:
            datos = {"mensaje": "El proveedor no existe"}

        return JsonResponse(datos)

    def put(self, request, id):
        pass


# VISTA DE SALIDA DETALLE


@method_decorator(csrf_exempt, name="dispatch")
class SalidadetalleView(View):
    def get(self, request, id=0, insumo=0):
        if id > 0:
            salidasdet = list(Salidadetalle.objects.filter(idsalida=id).values())
            if len(salidasdet) > 0:
                datos = {"mensaje": "exito", "salidas": salidasdet}
            else:
                datos = {"mensaje": "No se encontró el ID de salida"}
        else:
            if insumo:
                salidasdet = list(
                    Salidadetalle.objects.filter(idinsumo=insumo).values()
                )
            else:
                salidasdet = list(Salidadetalle.objects.values())

            if len(salidasdet) > 0:
                datos = {
                    "mensaje": "exito",
                    "cantidad": len(salidasdet),
                    "salidas": salidasdet,
                }
            else:
                datos = {"mensaje": "No se encontraron detalles de salida"}

        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        idsalida_id = jd["idsalida_id"]
        idinsumo_id = jd["idinsumo_id"]
        cantidad = jd["cantidad"]
        cantidad = int(cantidad)

        try:
            salida = Salida.objects.get(idsalida=idsalida_id)
        except Salida.DoesNotExist:
            salida = None

        if salida:
            try:
                insumo = Insumo.objects.get(idinsumo=idinsumo_id)
            except Insumo.DoesNotExist:
                insumo = None

            if insumo:
                if insumo.cantidad_disponible >= cantidad:
                    salidadetalle = Salidadetalle.objects.create(
                        idsalida=salida,
                        idinsumo=insumo,
                        cantidad=cantidad,
                        preciounitario=jd["preciounitario"],
                    )
                    datos = {"mensaje": "success"}
                else:
                    datos = {
                        "mensaje": "No hay suficiente stock disponible para realizar la salida"
                    }
            else:
                datos = {"mensaje": "El insumo no existe"}
        else:
            datos = {"mensaje": "La salida no existe"}
        return JsonResponse(datos)

    def put(self, request, id):
        pass