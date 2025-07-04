import os
from fpdf import FPDF
from datetime import datetime

class TestReportGenerator:
    def __init__(self, reports_folder='reports'):
        self.reports_folder = reports_folder
        self.ensure_reports_folder()
    
    def ensure_reports_folder(self):
        """Crea la carpeta de reportes si no existe"""
        if not os.path.exists(self.reports_folder):
            os.makedirs(self.reports_folder)
    
    def get_next_report_number(self):
        """Obtiene el siguiente número de reporte basado en archivos existentes"""
        existing_reports = [f for f in os.listdir(self.reports_folder) 
                          if f.startswith('test_report_') and f.endswith('.pdf')]
        
        if not existing_reports:
            return 1
        
        # Extraer números de los nombres de archivo existentes
        numbers = []
        for report in existing_reports:
            try:
                # Extraer número del formato "test_report_X.pdf"
                number = int(report.split('_')[2].split('.')[0])
                numbers.append(number)
            except (IndexError, ValueError):
                continue
        
        return max(numbers) + 1 if numbers else 1
    
    def clean_text_for_pdf(self, text):
        """Limpia el texto para que sea compatible con FPDF"""
        # Reemplazar emojis y caracteres especiales
        replacements = {
            '✅': '[OK]',
            '❌': '[ERROR]',
            '🎉': '[EXITO]',
            '🔧': '[SISTEMA]',
            '👤': '[USUARIO]',
            '📝': '[TAREA]',
            '📋': '[LISTA]',
            '👥': '[USUARIOS]'
        }
        
        for emoji, replacement in replacements.items():
            text = text.replace(emoji, replacement)
        
        return text
    
    def create_header(self, pdf, test_name):
        """Crea el encabezado del reporte"""
        # Título principal
        pdf.set_font("Arial", 'B', 18)
        pdf.set_fill_color(52, 73, 94)  # Azul oscuro
        pdf.cell(200, 15, txt="REPORTE DE PRUEBAS - LABORATORIO 2", ln=True, align='C', fill=True)
        pdf.ln(5)
        
        # Información del test
        pdf.set_font("Arial", 'B', 14)
        pdf.set_fill_color(41, 128, 185)  # Azul
        pdf.cell(200, 10, txt=f"Prueba: {test_name}", ln=True, align='C', fill=True)
        pdf.ln(5)
        
        # Información de fecha y hora
        pdf.set_font("Arial", '', 10)
        pdf.cell(100, 8, txt=f"Fecha: {datetime.now().strftime('%Y-%m-%d')}", ln=False)
        pdf.cell(100, 8, txt=f"Hora: {datetime.now().strftime('%H:%M:%S')}", ln=True)
        pdf.ln(5)
    
    def create_summary_table(self, pdf, execution_time, total_steps, passed_steps, failed_steps):
        """Crea tabla de resumen"""
        pdf.set_font("Arial", 'B', 12)
        pdf.set_fill_color(236, 240, 241)  # Gris claro
        pdf.cell(200, 10, txt="RESUMEN DE EJECUCION", ln=True, align='C', fill=True)
        pdf.ln(3)
        
        # Tabla de resumen
        pdf.set_font("Arial", 'B', 10)
        pdf.set_fill_color(52, 152, 219)  # Azul claro
        pdf.cell(50, 8, txt="METRICA", ln=False, align='C', fill=True)
        pdf.cell(50, 8, txt="VALOR", ln=False, align='C', fill=True)
        pdf.cell(50, 8, txt="ESTADO", ln=False, align='C', fill=True)
        pdf.cell(50, 8, txt="RESULTADO", ln=True, align='C', fill=True)
        
        pdf.set_font("Arial", '', 9)
        
        # Tiempo de ejecución
        pdf.cell(50, 8, txt="Tiempo de ejecucion", ln=False, align='C')
        pdf.cell(50, 8, txt=f"{execution_time:.2f}s", ln=False, align='C')
        pdf.cell(50, 8, txt="Completado", ln=False, align='C')
        pdf.cell(50, 8, txt="[OK]", ln=True, align='C')
        
        # Total de pasos
        pdf.cell(50, 8, txt="Total de pasos", ln=False, align='C')
        pdf.cell(50, 8, txt=str(total_steps), ln=False, align='C')
        pdf.cell(50, 8, txt="Ejecutados", ln=False, align='C')
        pdf.cell(50, 8, txt="[OK]", ln=True, align='C')
        
        # Pasos exitosos
        pdf.cell(50, 8, txt="Pasos exitosos", ln=False, align='C')
        pdf.cell(50, 8, txt=str(passed_steps), ln=False, align='C')
        pdf.cell(50, 8, txt="Completados", ln=False, align='C')
        pdf.cell(50, 8, txt="[OK]", ln=True, align='C')
        
        # Pasos fallidos
        if failed_steps > 0:
            pdf.cell(50, 8, txt="Pasos fallidos", ln=False, align='C')
            pdf.cell(50, 8, txt=str(failed_steps), ln=False, align='C')
            pdf.cell(50, 8, txt="Con errores", ln=False, align='C')
            pdf.cell(50, 8, txt="[ERROR]", ln=True, align='C')
        
        pdf.ln(5)
    
    def create_results_table(self, pdf, test_results):
        """Crea tabla con los resultados detallados"""
        pdf.set_font("Arial", 'B', 12)
        pdf.set_fill_color(236, 240, 241)  # Gris claro
        pdf.cell(200, 10, txt="DETALLE DE RESULTADOS", ln=True, align='C', fill=True)
        pdf.ln(3)
        
        # Encabezado de tabla
        pdf.set_font("Arial", 'B', 9)
        pdf.set_fill_color(52, 152, 219)  # Azul claro
        pdf.cell(20, 8, txt="PASO", ln=False, align='C', fill=True)
        pdf.cell(140, 8, txt="DESCRIPCION", ln=False, align='C', fill=True)
        pdf.cell(40, 8, txt="ESTADO", ln=True, align='C', fill=True)
        
        # Contenido de la tabla
        pdf.set_font("Arial", '', 8)
        step_number = 1
        
        for result in test_results:
            clean_result = self.clean_text_for_pdf(result)
            
            # Determinar estado basado en el contenido
            if '[OK]' in clean_result or '[EXITO]' in clean_result:
                status = "[OK]"
                fill_color = (46, 204, 113)  # Verde
            elif '[ERROR]' in clean_result:
                status = "[ERROR]"
                fill_color = (231, 76, 60)  # Rojo
            else:
                status = "[INFO]"
                fill_color = (52, 152, 219)  # Azul
            
            # Número de paso
            pdf.cell(20, 8, txt=str(step_number), ln=False, align='C')
            
            # Descripción (truncar si es muy larga)
            if len(clean_result) > 60:
                description = clean_result[:57] + "..."
            else:
                description = clean_result
            pdf.cell(140, 8, txt=description, ln=False, align='L')
            
            # Estado
            pdf.set_fill_color(*fill_color)
            pdf.cell(40, 8, txt=status, ln=True, align='C', fill=True)
            
            step_number += 1
        
        pdf.ln(5)
    
    def create_footer(self, pdf):
        """Crea el pie de página"""
        pdf.ln(10)
        pdf.set_font("Arial", 'I', 8)
        pdf.set_text_color(128, 128, 128)
        pdf.cell(200, 5, txt="Reporte generado automaticamente por el sistema de pruebas del Laboratorio 2", ln=True, align='C')
        pdf.cell(200, 5, txt="Estudiante: Laura Valentina Pabon Cabezas - ID: 1001175750", ln=True, align='C')
    
    def generate_report(self, test_name, test_results, execution_time=None):
        """Genera un reporte PDF con los resultados de la prueba"""
        pdf = FPDF()
        pdf.add_page()
        
        # Crear encabezado
        self.create_header(pdf, test_name)
        
        # Calcular estadísticas
        total_steps = len(test_results)
        passed_steps = sum(1 for result in test_results if '[OK]' in result or '[EXITO]' in result)
        failed_steps = sum(1 for result in test_results if '[ERROR]' in result)
        
        # Crear tabla de resumen
        self.create_summary_table(pdf, execution_time or 0, total_steps, passed_steps, failed_steps)
        
        # Crear tabla de resultados detallados
        self.create_results_table(pdf, test_results)
        
        # Crear pie de página
        self.create_footer(pdf)
        
        # Generar nombre de archivo con número secuencial
        report_number = self.get_next_report_number()
        filename = f"test_report_{report_number}.pdf"
        filepath = os.path.join(self.reports_folder, filename)
        
        # Guardar PDF
        pdf.output(filepath)
        print(f"[OK] Reporte PDF generado: {filepath}")
        
        return filepath

def generate_backend_test_report(test_results, execution_time=None):
    """Función helper para generar reporte de pruebas de backend"""
    generator = TestReportGenerator()
    return generator.generate_report("Backend Integration Test", test_results, execution_time)

def generate_frontend_test_report(test_results, execution_time=None):
    """Función helper para generar reporte de pruebas de frontend"""
    generator = TestReportGenerator()
    return generator.generate_report("Frontend E2E Test", test_results, execution_time) 