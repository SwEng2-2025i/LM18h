import os
import glob
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet

class PDFReportGenerator:
    def __init__(self, reports_dir="Test/Reports"):
        self.reports_dir = reports_dir
        # Crear directorio si no existe
        os.makedirs(reports_dir, exist_ok=True)
    
    def _get_next_report_number(self):
        """Get the next sequential report number"""
        existing_reports = glob.glob(os.path.join(self.reports_dir, "report_*.pdf"))
        if not existing_reports:
            return 1
        
        # Extract numbers from existing reports
        numbers = []
        for report in existing_reports:
            filename = os.path.basename(report)
            try:
                # Extract number from "report_XXX.pdf"
                number = int(filename.split('_')[1].split('.')[0])
                numbers.append(number)
            except (IndexError, ValueError):
                continue
        
        return max(numbers) + 1 if numbers else 1
    
    def generate_report(self, test_type, test_results, execution_time=None):
        """Generate simple PDF report with test results"""
        report_number = self._get_next_report_number()
        filename = f"report_{report_number:03d}.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        story.append(Paragraph(f"Integration Test Report #{report_number:03d}", styles['Title']))
        story.append(Spacer(1, 20))
        
        # Test Information
        story.append(Paragraph("Test Information", styles['Heading2']))
        info_data = [
            ['Test Type:', test_type],
            ['Execution Date:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ['Report Number:', f"#{report_number:03d}"],
        ]
        
        if execution_time:
            info_data.append(['Execution Time:', f"{execution_time:.2f} seconds"])
        
        info_table = Table(info_data)
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Overall Status
        overall_status = "PASSED" if test_results.get('overall_success', False) else "FAILED"
        story.append(Paragraph(f"Overall Status: {overall_status}", styles['Heading3']))
        story.append(Spacer(1, 10))
        
        # Test Results
        story.append(Paragraph("Test Results", styles['Heading2']))
        results_data = [['Step', 'Description', 'Status', 'Details']]
        
        for step in test_results.get('steps', []):
            status = "PASS" if step.get('success', False) else "FAIL"
            results_data.append([
                str(step.get('step_number', '')),
                step.get('description', ''),
                status,
                step.get('details', '')
            ])
        
        results_table = Table(results_data)
        story.append(results_table)
        story.append(Spacer(1, 20))
        
        # Data Cleanup
        if test_results.get('cleanup'):
            story.append(Paragraph("Data Cleanup", styles['Heading2']))
            cleanup_data = [['Action', 'Status', 'Details']]
            
            for action in test_results['cleanup']:
                status = "SUCCESS" if action.get('success', False) else "FAILED"
                cleanup_data.append([
                    action.get('action', ''),
                    status,
                    action.get('details', '')
                ])
            
            cleanup_table = Table(cleanup_data)
            story.append(cleanup_table)
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        print(f"PDF Report generated: {filepath}")
        return filepath