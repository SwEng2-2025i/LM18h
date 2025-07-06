from fpdf import FPDF
import os

class GeneradorReportePDF:
    def __init__(self, descripcion):
        self.descripcion = descripcion
        self.lineas_reporte = []

    def agregar_linea(self, linea):
        self.lineas_reporte.append(linea)

    def generar(self, carpeta="reportes"):
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        
        archivos = os.listdir(carpeta)
        numero_reporte = 1
        while f"reporte_{numero_reporte}.pdf" in archivos:
            numero_reporte += 1
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt=self.descripcion, ln=True, align='C')
        
        for linea in self.lineas_reporte:
            pdf.multi_cell(0, 10, txt=linea)
            
        pdf.output(os.path.join(carpeta, f"reporte_{numero_reporte}.pdf")) 