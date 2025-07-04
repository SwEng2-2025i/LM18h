from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import os
import glob

class TestReport:
    def __init__(self, test_name):
        self.test_name = test_name
        self.start_time = datetime.now()
        self.end_time = None
        self.logs = []
        self.success = True
        
        # Create reports directory if it doesn't exist
        self.reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Get next report number
        existing_reports = glob.glob(os.path.join(self.reports_dir, 'test_report_*.pdf'))
        self.report_number = len(existing_reports) + 1

    def add_log(self, message, success=True):
        timestamp = datetime.now()
        self.logs.append({
            'timestamp': timestamp,
            'message': message,
            'success': success
        })
        if not success:
            self.success = False
        print(f"{'✅' if success else '❌'} {message}")

    def end_test(self):
        self.end_time = datetime.now()

    def generate_pdf(self):
        # Create PDF filename with sequential number
        filename = os.path.join(self.reports_dir, f'test_report_{self.report_number:03d}.pdf')
        
        # Create the PDF document
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Create custom styles
        styles.add(ParagraphStyle(
            name='Success',
            parent=styles['Normal'],
            textColor=colors.green
        ))
        styles.add(ParagraphStyle(
            name='Error',
            parent=styles['Normal'],
            textColor=colors.red
        ))
        
        # Build the PDF content
        content = []
        
        # Add title
        content.append(Paragraph(f"Test Report #{self.report_number:03d}", styles['Title']))
        content.append(Spacer(1, 12))
        
        # Add test information
        content.append(Paragraph(f"Test Name: {self.test_name}", styles['Heading2']))
        content.append(Paragraph(f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        if self.end_time:
            duration = self.end_time - self.start_time
            content.append(Paragraph(f"End Time: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            content.append(Paragraph(f"Duration: {duration.total_seconds():.2f} seconds", styles['Normal']))
        
        # Add overall status
        status_style = 'Success' if self.success else 'Error'
        status_text = 'PASSED' if self.success else 'FAILED'
        content.append(Spacer(1, 12))
        content.append(Paragraph(f"Status: {status_text}", styles[status_style]))
        content.append(Spacer(1, 12))
        
        # Add logs table
        if self.logs:
            content.append(Paragraph("Test Logs:", styles['Heading2']))
            content.append(Spacer(1, 12))
            
            # Create table data
            table_data = [['Time', 'Message', 'Status']]
            for log in self.logs:
                time_str = log['timestamp'].strftime('%H:%M:%S')
                status = '✓' if log['success'] else '✗'
                table_data.append([time_str, log['message'], status])
            
            # Create and style the table
            table = Table(table_data, colWidths=[70, 400, 50])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            content.append(table)
        
        # Build the PDF
        doc.build(content)
        print(f"✅ Report generated: {filename}")
        return filename 