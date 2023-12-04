
import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from common.models import Coccion, Receta, Insumo, Recetadetalle
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.http import HttpResponse
from django.views import View
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from django.db.models import Count


class CoccionView(View):

    @method_decorator(csrf_exempt, name='dispatch')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, receta=0):
        if receta > 0:
            cocciones = list(Coccion.objects.filter(receta=receta).values())
            if cocciones > 0:
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
        receta_id = jd["receta_id"]
        insuficientes = list()

        try:
            receta = Receta.objects.get(nombre_receta=receta_id)
        except Receta.DoesNotExist:
            receta = None

        if receta:
            detalles = Recetadetalle.objects.filter(receta=receta.nombre_receta)
            for detalle in detalles:
                gasto = detalle.cantidad
                print('esto es gasto', gasto)
                insumo = Insumo.objects.filter(nombre_insumo=detalle.insumo.nombre_insumo).get()
                stock = insumo.cantidad_disponible
                print('esto es stock', stock)
                if gasto>stock:
                    nombre=str(detalle.insumo.nombre_insumo)
                    insuficientes.append(nombre)
            if insuficientes:
                mensaje = f'No hay suficiente stock de {", ".join(insuficientes)}'
                return JsonResponse({'message': mensaje}, status=400)
            else:
                coccion = Coccion.objects.create(receta=receta, fecha_coccion=jd["fecha_coccion"])
                datos = {"message": "success"}
                return JsonResponse(datos, status=200)
        else:
            datos = {'message': 'No se encontró la receta'}
            return JsonResponse(datos, status=400)
        
class InformeCoccionesView(View):
    
    def cantCocciones(self):
        cocciones = list(Coccion.objects.filter())
        cantidad = len(cocciones)
        return cantidad
    
    # Informe
    def get(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="informe_cocciones.pdf"'
        p = canvas.Canvas(response, pagesize=A4)
        p.translate(inch, inch)

        # CABECERA
        p.setStrokeColorRGB(0,0,0)
        p.setLineWidth(1)
        p.line(-1*inch,9*inch,8*inch,9*inch)
        p.setFillColorRGB(0, 0, 0)
        p.setFont('Helvetica-Bold', 20)
        p.drawString(1.5*inch, 9.25 * inch, 'Informe Cocciones:')
        p.setFont('Helvetica', 12)
        p.drawString(5*inch, 10.25 * inch, f'{datetime.date.today()}')
        p.drawString(-0.75*inch,10.25*inch, "Fábrica de Cervezas Del Barco")

        #CUERPO
        p.setFont('Helvetica-Bold', 14)
        p.drawString(-0.75*inch, 8.5 * inch, f'Cantidad de Cocciones: {self.cantCocciones()}')
        p.setFont('Helvetica', 12)
        p.drawString(-0.75*inch, 1 * inch, 'Este es un párrafo al final del informe.')

        # GRAFICO
        recetas = []
        cantidades = []
        cocciones = Coccion.objects.values('receta').annotate(cantidad=Count('receta'))
        listacocciones = list(cocciones)
        for coccion in listacocciones:
            recetas.append(f'{coccion["receta"]}: {coccion["cantidad"]}')
            long = len(listacocciones)
            porcentaje = (coccion['cantidad'] * 100)/long
            cantidades.append(porcentaje)
        d = Drawing(200, 100)
        pc = Pie()
        pc.width = 200
        pc.height = 200
        pc.data = cantidades
        pc.labels = recetas
        pc.sideLabels=1
        pc.slices.strokeWidth=0.5
        d.add(pc)
        d.drawOn(p, inch, 5*inch)
        p.showPage()
        
        p.save()
        
        return response