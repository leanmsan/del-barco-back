import datetime
import json
from typing import Any
from django import http
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from common.models import Insumo, Proveedor
from django.views import View
from django.http.response import JsonResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch, cm, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
from django.views import View
from reportlab.lib.utils import ImageReader

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
        
        try:
            insumo = Insumo.objects.get(idinsumo=id)
        except Insumo.DoesNotExist:
            datos = {'message': 'No se encontró el insumo'}
            return JsonResponse(datos, status=404)
        
        nombre_insumo = jd.get('nombre_insumo', None)
        if nombre_insumo:
            insumos_con_mismo_nombre = Insumo.objects.filter(nombre_insumo=nombre_insumo).exclude(idinsumo=id)
            if insumos_con_mismo_nombre.exists():
                datos = {'message': 'El nombre ya existe en otro insumo. No se puede actualizar.'}
                return JsonResponse(datos, status=400)

        
        proveedor_id = jd.get('proveedor_id', None)
        
        if proveedor_id:
            try:
                proveedor_real = Proveedor.objects.get(nombre_proveedor=proveedor_id)
                insumo.proveedor = proveedor_real
            except Proveedor.DoesNotExist:
                datos = {'message': 'El proveedor proporcionado no existe'}
                return JsonResponse(datos, status=404)
            
        for field_name, field_value in jd.items():
            if field_name != 'proveedor_id' and hasattr(insumo, field_name):
                setattr(insumo, field_name, field_value)
        insumo.save()

        datos = {'message': 'Insumo actualizado correctamente'}
        return JsonResponse(datos, status= 200)
    
    
class InformeInsumosView(View):
    
    def valoracion_stock(self):
        valoracion = 0
        insumos = Insumo.objects.filter()
        for insumo in insumos:
            valoracion += (insumo.cantidad_disponible * insumo.precio_unitario)
        return valoracion
    
    
    def filtroInsumos(self, categoria=None):
        if categoria:
            insumos = Insumo.objects.filter(categoria=categoria).values_list('nombre_insumo', 'cantidad_disponible', 'tipo_medida','precio_unitario', 'proveedor', 'categoria')
        else:
           insumos = Insumo.objects.filter().values_list('nombre_insumo', 'cantidad_disponible', 'tipo_medida','precio_unitario', 'proveedor', 'categoria') 
        lista = list(insumos)
        lista.insert(0,['Nombre', 'Stock', 'Medida','Precio', 'Proveedor', 'Categoria'])
        
        return lista
    
    # Informe
    def get(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="informe_insumos.pdf"'
        fecha = datetime.date.today()
        fecha = fecha.strftime("%d/%m/%Y")
        p = canvas.Canvas(response, pagesize=A4)
        p.translate(inch, inch)
        
        # CABECERA
        p.setStrokeColorRGB(0,0,0)
        p.setLineWidth(1)
        p.line(-1*inch,9*inch,8*inch,9*inch)
        p.setFillColorRGB(0, 0, 0)
        p.setFont('Helvetica-Bold', 20)
        p.drawString(1.5*inch, 9.25 * inch, 'Informe Insumos:')
        p.setFont('Helvetica', 12)
        p.drawString(5*inch, 10.25 * inch, f'{fecha}')
        p.drawString(-0.75*inch,10.25*inch, "Fábrica de Cervezas Del Barco")

        
        # CUERPO
        p.drawString(-0.75*inch, 8.5 * inch, 'Tabla: ')
        data = self.filtroInsumos()
        tabla = Table(data)

        estilo_tabla = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#1f77b4'),
                           ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                           ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                           ('BACKGROUND', (0, 1), (-1, -1), '#f0f0f0')])
        tabla.setStyle(estilo_tabla)
        tabla.wrapOn(p, 0, 0)
        tabla.drawOn(p, 0*inch, 5*inch)
        p.drawString(100, 150, "")
        p.setFont("Helvetica", 16)
        p.drawString(-0.75*inch, 4 * inch, "Valoración actual del Stock:")
        p.drawString(-0.5*inch, 3.5 * inch, f"Total:   ${self.valoracion_stock()}")

        p.showPage()
        
        p.save()
        return response