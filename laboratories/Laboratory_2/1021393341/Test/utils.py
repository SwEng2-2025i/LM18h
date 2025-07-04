# utils.py
import os
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

class TestResult:
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = "NO EJECUTADO"
        self.mensaje = ""
        self.excepcion = None

    def pasar(self, mensaje=""):
        self.estado = "✅ PASÓ"
        self.mensaje = mensaje

    def fallar(self, mensaje="", excepcion=None):
        self.estado = "❌ FALLÓ"
        self.mensaje = mensaje
        self.excepcion = excepcion

def generar_reporte_pdf(resultados, carpeta="reports"):
    os.makedirs(carpeta, exist_ok=True)
    existentes = [f for f in os.listdir(carpeta) if f.startswith("reporte_") and f.endswith(".pdf")]
    indices = [int(f.replace("reporte_", "").replace(".pdf", "")) for f in existentes if f.replace("reporte_", "").replace(".pdf", "").isdigit()]
    nuevo_indice = max(indices, default=0) + 1
    nombre_pdf = os.path.join(carpeta, f"reporte_{nuevo_indice}.pdf")

    c = canvas.Canvas(nombre_pdf, pagesize=LETTER)
    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Reporte de Pruebas - #{nuevo_indice}")
    c.drawString(50, 755, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.line(50, 750, 550, 750)

    y = 730
    total = len(resultados)
    pasados = sum(1 for r in resultados if r.estado == "✅ PASÓ")
    fallidos = sum(1 for r in resultados if r.estado == "❌ FALLÓ")

    for r in resultados:
        if y < 100:
            c.showPage()
            y = 770
            c.setFont("Helvetica", 12)
        c.drawString(50, y, f"{r.nombre}: {r.estado}")
        y -= 18
        c.drawString(70, y, f"- Descripción: {r.descripcion}")
        y -= 18
        if r.mensaje:
            c.drawString(70, y, f"- Mensaje: {r.mensaje}")
            y -= 18
        if r.excepcion:
            c.drawString(70, y, f"- Excepción: {r.excepcion}")
            y -= 18
        y -= 10

    c.drawString(50, y-10, f"Resumen Final: {total} pruebas ejecutadas / {pasados} PASADAS / {fallidos} FALLIDAS")
    c.save()
    print(f"✅ PDF generado: {nombre_pdf}")
