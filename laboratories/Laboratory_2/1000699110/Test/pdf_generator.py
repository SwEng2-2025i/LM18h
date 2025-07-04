"""
Generator of PDF reports for test results.
Generates sequentially numbered PDFs without overwriting previous files.
"""

import os
import glob
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

class TestReportGenerator:
    def __init__(self, reports_dir="Test/Reports"):
        """
        Initializes the report generator.
        
        Args:
            reports_dir (str): Directory where PDFs will be saved
        """
        self.reports_dir = reports_dir
        self.ensure_reports_directory()
    
    def ensure_reports_directory(self):
        """Creates the reports directory if it doesn't exist"""
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
            print(f"📁 Reports directory created: {self.reports_dir}")

    def get_next_report_number(self):
        """
        Obtains the next sequential number for the report.

        Returns:
            int: The next report number
        """
        # Search for all existing PDF files
        pattern = os.path.join(self.reports_dir, "test_report_*.pdf")
        existing_files = glob.glob(pattern)
        
        if not existing_files:
            return 1

        # Extract numbers from existing files
        numbers = []
        for file_path in existing_files:
            filename = os.path.basename(file_path)
            try:
                # Extract number from format: test_report_001.pdf
                number_part = filename.split('_')[-1].split('.')[0]
                numbers.append(int(number_part))
            except (ValueError, IndexError):
                continue
        
        return max(numbers) + 1 if numbers else 1
    
    def generate_filename(self, report_number):
        """
        Generates the PDF filename.

        Args:
            report_number (int): Report number

        Returns:
            str: Full path of the PDF file
        """
        filename = f"test_report_{report_number:03d}.pdf"
        return os.path.join(self.reports_dir, filename)
    
    def create_styles(self):
        """Creates the styles for the PDF document"""
        styles = getSampleStyleSheet()

        # Style for the title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=TA_CENTER
        )

        # Style for subtitles
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkgreen,
            alignment=TA_LEFT
        )

        # Style for normal text
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_LEFT
        )

        # Style for success
        success_style = ParagraphStyle(
            'Success',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.green,
            spaceAfter=6
        )

        # Style for error
        error_style = ParagraphStyle(
            'Error',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.red,
            spaceAfter=6
        )
        
        return {
            'title': title_style,
            'subtitle': subtitle_style,
            'normal': normal_style,
            'success': success_style,
            'error': error_style
        }
    
    def generate_pdf_report(self, test_results):
        """
        Generates a PDF with the test results.

        Args:
            test_results (dict): Dictionary with the test results

        Returns:
            str: Full path of the generated PDF file
        """
        report_number = self.get_next_report_number()
        filename = self.generate_filename(report_number)

        # Create the PDF document
        doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=1*inch)

        # Get styles
        styles = self.create_styles()

        # Build the content of the document
        story = []
        
        # Main Title
        title = f"Reporte de Tests #{report_number:03d}"
        story.append(Paragraph(title, styles['title']))
        story.append(Spacer(1, 20))
        
        # General Information
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info_data = [
            ['Fecha y Hora:', timestamp],
            ['Número de Reporte:', f"#{report_number:03d}"],
            ['Total de Tests:', str(test_results.get('total_tests', 0))],
            ['Tests Exitosos:', str(test_results.get('successful_tests', 0))],
            ['Tests Fallidos:', str(test_results.get('failed_tests', 0))]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Results of each test
        if 'test_details' in test_results:
            story.append(Paragraph("Detalle de Tests Ejecutados", styles['subtitle']))
            story.append(Spacer(1, 10))
            
            for test_detail in test_results['test_details']:
                test_name = test_detail.get('name', 'Test Desconocido')
                test_status = test_detail.get('status', 'unknown')
                test_duration = test_detail.get('duration', 'N/A')
                test_output = test_detail.get('output', '')
                test_error = test_detail.get('error', '')
                
                # Test name
                story.append(Paragraph(f"Test: {test_name}", styles['subtitle']))

                # Status and duration
                status_color = 'success' if test_status == 'passed' else 'error'
                status_text = "✅ EXITOSO" if test_status == 'passed' else "❌ FALLIDO"
                story.append(Paragraph(f"Estado: {status_text}", styles[status_color]))
                story.append(Paragraph(f"Duración: {test_duration}", styles['normal']))
                
                # Test output
                if test_output:
                    story.append(Paragraph("Salida del Test:", styles['normal']))
                    output_lines = test_output.split('\n')
                    for line in output_lines[:10]:  # Limitar a 10 líneas
                        if line.strip():
                            story.append(Paragraph(f"  {line}", styles['normal']))

                # Errors if any
                if test_error:
                    story.append(Paragraph("Errores:", styles['error']))
                    error_lines = test_error.split('\n')
                    for line in error_lines[:5]:  # Limitar a 5 líneas
                        if line.strip():
                            story.append(Paragraph(f"  {line}", styles['error']))
                
                story.append(Spacer(1, 15))
        
        # Final Summary
        story.append(Paragraph("Resumen Final", styles['subtitle']))
        
        total_tests = test_results.get('total_tests', 0)
        successful_tests = test_results.get('successful_tests', 0)
        
        if total_tests > 0:
            success_rate = (successful_tests / total_tests) * 100
            summary_style = 'success' if success_rate >= 80 else 'error'
            story.append(Paragraph(f"Tasa de Éxito: {success_rate:.1f}%", styles[summary_style]))
        
        # Generate the PDF
        doc.build(story)
        
        print(f"📄 Reporte PDF generado: {filename}")
        return filename

# Convenience functions for use in tests
def create_test_result(name, status, duration=None, output="", error=""):
    """
    Create a test result dictionary.

    Args:
        name (str): Test name
        status (str): 'passed' or 'failed'
        duration (str): Test duration
        output (str): Test output
        error (str): Error messages if any

    Returns:
        dict: Dictionary with test data
    """
    return {
        'name': name,
        'status': status,
        'duration': duration,
        'output': output,
        'error': error
    }

def generate_test_report(test_details, reports_dir="LM18h/laboratories/Laboratory_2/1000699110/Test/Reports"):
    """
    Convenience function to generate a report.

    Args:
        test_details (list): List of dictionaries with test results
        reports_dir (str): Directory to save the report

    Returns:
        str: Path of the generated PDF file
    """
    # Calculate statistics
    total_tests = len(test_details)
    successful_tests = sum(1 for test in test_details if test.get('status') == 'passed')
    failed_tests = total_tests - successful_tests
    
    test_results = {
        'total_tests': total_tests,
        'successful_tests': successful_tests,
        'failed_tests': failed_tests,
        'test_details': test_details
    }
    
    generator = TestReportGenerator(reports_dir)
    return generator.generate_pdf_report(test_results)
