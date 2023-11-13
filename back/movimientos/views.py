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

# VISTA DE ENTRADA

@method_decorator(csrf_exempt, name="dispatch")
class EntradaView(View):
    def get(self, request, id=0, prov=None):
        if id > 0:
            entradas = list(Entrada.objects.filter(identrada=id).values())
            if len(entradas) > 0:
                entrada = entradas[0]
                datos = {"message": "exito", "entrada": entrada}
            else:
                datos = {"message": "No se encontró el movimiento de entrada"}
        else:
            entradas = list(Entrada.objects.values())
            if len(entradas) > 0:
                datos = {
                    "message": "exito", "cantidad": len(entradas), "entradas": entradas}
            else:
                datos = {"message": "No se encontraron movimientos de entrada"}
        return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        proveedor_id = jd["proveedor_id"]
        montoTotal = jd["monto_total"]
        
        try:
            proveedor = Proveedor.objects.get(nombre_proveedor=proveedor_id)
        except Proveedor.DoesNotExist:
            proveedor = None

        if proveedor:
            entrada = Entrada.objects.create(proveedor=proveedor, fecha_entrada=jd["fecha_entrada"], monto_total=montoTotal)
            last_inserted_id = entrada.identrada
            datos = {"message": "success", "last_inserted_id": last_inserted_id}
        else:
            datos = {"message": "El proveedor no existe"}
            return JsonResponse(datos, status=400)
        
        return JsonResponse(datos)

    def patch(self, request, id):
        pass

@method_decorator(csrf_exempt, name="dispatch")
class GetLastIdEntradaView(View):
    #get para obtener el ultimo id
    def get(self, request):
        entrada = Entrada.objects.latest('identrada')
        lastId = entrada.identrada
        lastIdEntrada = {"message": "exito", "lastid": lastId}
        return JsonResponse(lastIdEntrada)

# VISTA DE ENTRADA DETALLE

@method_decorator(csrf_exempt, name="dispatch")
class EntradadetalleView(View):
    def get(self, request, id=0):
        if id > 0:
            entradasdet = list(Entradadetalle.objects.filter(identrada=id).values())
            if len(entradasdet):
                datos = {"message": "exito", "entradas": entradasdet}
                return JsonResponse(datos, status=200)
            else:
                datos = {"message": "No se encontró el id de entrada"}
                return JsonResponse(datos, status=404)
        else:
            entradasdet = list(Entradadetalle.objects.values())
            if len(entradasdet) > 0:
                datos = {
                    "message": "exito",
                    "cantidad": len(entradasdet),
                    "entradas": entradasdet,
                }
                return JsonResponse(datos, status=200)
            else:
                datos = {"message": "No se encontraron detalles de entrada"}
                return JsonResponse(datos, status=404)

    def post(self, request):
        jd = json.loads(request.body)
        identrada_id = jd["identrada_id"]
        insumo_id = jd["insumo_id"]
        cantidad = jd["cantidad"]
        try:
            identrada = Entrada.objects.get(identrada=int(identrada_id))
        except Entrada.DoesNotExist:
            identrada = None

        if identrada:
            try:
                insumo = Insumo.objects.get(nombre_insumo=insumo_id)
            except Insumo.DoesNotExist:
                insumo = None

            if insumo:
                entrada = Entradadetalle.objects.create(
                    identrada=identrada,
                    insumo=insumo,
                    cantidad=cantidad,
                    precio_unitario=jd["precio_unitario"]
                )
                datos = {"message": "success"}
                return JsonResponse(datos, status=200)
            else:
                datos = {"message": "El insumo no existe"}
                return JsonResponse(datos, status=400)
        else:
            datos = {"message": "La entrada no existe"}
            return JsonResponse(datos, status=400)

    def put(self, request, id):
        pass


# VISTA DE SALIDA


@method_decorator(csrf_exempt, name="dispatch")
class SalidaView(View):
    def get(self, request, id=0):
        if id > 0:
            salidas = list(Salida.objects.filter(idsalida=id).values())
            if len(salidas) > 0:
                salida = salidas[0]
                datos = {"message": "exito", "salida": salida}
                return JsonResponse(datos, status=200)
            else:
                datos = {"message": "No se encontró el movimiento de salida"}
                return JsonResponse(datos, status=404)
        else:
            salidas = list(Salida.objects.values())
            if len(salidas) > 0:
                datos = {
                    "message": "exito",
                    "cantidad": len(salidas),
                    "salidas": salidas,
                }
                return JsonResponse(datos, status=200)
            else:
                datos = {"message": "No se encontraron movimientos de salida"}
                return JsonResponse(datos, status=400)

    def post(self, request):
        jd = json.loads(request.body)
        salida = Salida.objects.create(fecha_salida=jd["fecha_salida"], descripcion=jd.get("descripcion", None))
        last_inserted_id = salida.idsalida
        datos = {"message": "success", "last_inserted_id": last_inserted_id}
        return JsonResponse(datos, status=200)


    def put(self, request, id):
        pass


@method_decorator(csrf_exempt, name="dispatch")
class GetLastIdSalidaView(View):
    #get para obtener el ultimo id
    def get(self, request):
        salida = Salida.objects.latest('idsalida')
        lastId = salida.idsalida
        lastIdSalida = {"message": "exito", "lastid": lastId}
        return JsonResponse(lastIdSalida)



# VISTA DE SALIDA DETALLE

@method_decorator(csrf_exempt, name="dispatch")
class SalidadetalleView(View):
    def get(self, request, id=0):
        if id > 0:
            salidasdet = list(Salidadetalle.objects.filter(idsalida=id).values())
            if len(salidasdet):
                datos = {"message": "exito", "salidas": salidasdet}
                return JsonResponse(datos, status=200)
            else:
                datos = {"message": "No se encontró el id de salida"}
                return JsonResponse(datos, status=404)
        else:
            salidasdet = list(Salidadetalle.objects.values())
            if len(salidasdet) > 0:
                datos = {
                    "message": "exito",
                    "cantidad": len(salidasdet),
                    "salidas": salidasdet,
                }
                return JsonResponse(datos, status=200)
            else:
                datos = {"message": "No se encontraron detalles de salida"}
                return JsonResponse(datos, status=404)

    def post(self, request):
        jd = json.loads(request.body)
        idsalida_id = jd["idsalida_id"]
        insumo_id = jd["insumo_id"]
        cantidad = jd["cantidad"]
        cantidad = int(cantidad)
        try:
            idsalida = Salida.objects.get(idsalida=int(idsalida_id))
        except Salida.DoesNotExist:
            idsalida = None

        if idsalida:
            try:
                insumo = Insumo.objects.get(nombre_insumo=insumo_id)
            except Insumo.DoesNotExist:
                insumo = None

            if insumo:
                if insumo.cantidad_disponible >= cantidad:
                    salida = Salidadetalle.objects.create(
                        idsalida=idsalida,
                        insumo=insumo,
                        cantidad=cantidad
                    )
                    insumo.cantidad_disponible -= cantidad
                    insumo.save
                    datos = {"message": "success"}
                    return JsonResponse(datos, status=200)
                else:
                    datos = {"message": "No hay suficiente stock de este insumo"}
                    return JsonResponse(datos, status=400)
            else:
                datos = {"message": "El insumo no existe"}
                return JsonResponse(datos, status=400)
        else:
            datos = {"message": "La salida no existe"}
            return JsonResponse(datos, status=400)

    def put(self, request, id):
        pass
