import os
import glob
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

class PDFReportGenerator:
    def __init__(self, reports_dir="reports"):
        self.reports_dir = reports_dir
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
    
    def get_next_report_number(self):
        """Get the next sequential report number"""
        existing_reports = glob.glob(os.path.join(self.reports_dir, "test_report_*.pdf"))
        if not existing_reports:
            return 1
        
        numbers = []
        for report in existing_reports:
            try:
                # Extract number from filename like "test_report_001.pdf"
                basename = os.path.basename(report)
                number_str = basename.split('_')[2].split('.')[0]
                numbers.append(int(number_str))
            except (IndexError, ValueError):
                continue
        
        return max(numbers) + 1 if numbers else 1
    
    def generate_report(self, test_type, test_results, created_data=None, cleanup_results=None):
        """Generate PDF report for test results"""
        report_number = self.get_next_report_number()
        filename = f"test_report_{report_number:03d}.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            textColor=colors.darkblue
        )
        
        # Title
        title = Paragraph(f"Test Report #{report_number:03d} - {test_type}", title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Test execution info
        exec_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        info_text = f"<b>Test Type:</b> {test_type}<br/><b>Execution Time:</b> {exec_time}<br/><b>Report Number:</b> {report_number}"
        story.append(Paragraph(info_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Test Results Summary
        story.append(Paragraph("<b>Test Results Summary:</b>", styles['Heading2']))
        
        # Create results table
        results_data = [['Test Step', 'Status', 'Details']]
        for result in test_results:
            status = "✅ PASS" if result['status'] == 'PASS' else "❌ FAIL"
            results_data.append([result['step'], status, result['details']])
        
        results_table = Table(results_data, colWidths=[2*inch, 1*inch, 3*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(results_table)
        story.append(Spacer(1, 20))
        
        # Created data section
        if created_data:
            story.append(Paragraph("<b>Data Created During Test:</b>", styles['Heading2']))
            created_text = ""
            for key, value in created_data.items():
                created_text += f"<b>{key}:</b> {value}<br/>"
            story.append(Paragraph(created_text, styles['Normal']))
            story.append(Spacer(1, 20))
        
        # Cleanup results section
        if cleanup_results:
            story.append(Paragraph("<b>Data Cleanup Results:</b>", styles['Heading2']))
            cleanup_data = [['Operation', 'Status', 'Details']]
            for cleanup in cleanup_results:
                status = "✅ SUCCESS" if cleanup['status'] == 'SUCCESS' else "❌ FAILED"
                cleanup_data.append([cleanup['operation'], status, cleanup['details']])
            
            cleanup_table = Table(cleanup_data, colWidths=[2*inch, 1*inch, 3*inch])
            cleanup_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(cleanup_table)
        
        # Build PDF
        doc.build(story)
        
        print(f"📄 PDF Report generated: {filepath}")
        return filepath
