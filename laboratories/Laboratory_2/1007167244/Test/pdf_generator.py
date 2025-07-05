import os
from fpdf import FPDF
from datetime import datetime

class TestReportGenerator:
    def __init__(self, test_type):
        self.test_type = test_type
        self.report_dir = os.path.dirname(os.path.abspath(__file__))
    
    def get_next_report_number(self):
        """Obtener el siguiente número secuencial de reporte"""
        existing_reports = []
        for file in os.listdir(self.report_dir):
            if file.startswith(f"{self.test_type}-report_") and file.endswith(".pdf"):
                try:
                    number = int(file.split("_")[1].split(".")[0])
                    existing_reports.append(number)
                except:
                    continue
        
        if not existing_reports:
            return 1
        return max(existing_reports) + 1
    
    def generate_report(self, test_results):
        """Generar reporte PDF con resultados de pruebas"""
        pdf = FPDF()
        pdf.add_page()
        
        # Título
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f'Reporte de Prueba de Integración {self.test_type}', ln=True, align='C')
        pdf.ln(10)
        
        # Información de la prueba
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Información de la Prueba:', ln=True)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 8, f'Tipo de Prueba: {self.test_type}', ln=True)
        pdf.cell(0, 8, f'Fecha y Hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', ln=True)
        pdf.ln(5)
        
        # Resultados de la prueba
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Resultados de la Prueba:', ln=True)
        pdf.set_font('Arial', '', 10)
        
        for key, value in test_results.items():
            if key == 'status':
                color = 'VERDE' if value == 'PASS' else 'ROJO'
                pdf.set_text_color(0, 128, 0) if value == 'PASS' else pdf.set_text_color(255, 0, 0)
                pdf.cell(0, 8, f'{key}: {value}', ln=True)
                pdf.set_text_color(0, 0, 0)  # Restablecer color
            else:
                pdf.cell(0, 8, f'{key}: {value}', ln=True)
        
        # Guardar reporte
        report_number = self.get_next_report_number()
        filename = f"{self.test_type}-report_{report_number}.pdf"
        filepath = os.path.join(self.report_dir, filename)
        pdf.output(filepath)
        
        print(f"📄 Reporte PDF generado: {filename}")
        return filepath 