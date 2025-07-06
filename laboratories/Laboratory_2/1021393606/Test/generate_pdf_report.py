from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def save_pdf_report(report_data, report_title="Test Report", report_type="General Test"):
    os.makedirs("pdf_reports", exist_ok=True)
    existing = [f for f in os.listdir("pdf_reports") if f.startswith("report_") and f.endswith(".pdf")]
    report_number = len(existing) + 1
    filename = f"pdf_reports/report_{report_number:03}.pdf"

    c = canvas.Canvas(filename, pagesize=LETTER)
    width, height = LETTER
    y = height - 50

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"{report_title} #{report_number}")
    y -= 30

    # General Info
    c.setFont("Helvetica", 12)
    execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(50, y, f"Test Type: {report_type}")
    y -= 20
    c.drawString(50, y, f"Execution Time: {execution_time}")
    y -= 20
    c.drawString(50, y, f"Report Number: {report_number}")
    y -= 40

    # Test Results Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Test Results Summary:")
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Test Step")
    c.drawString(250, y, "Status")
    c.drawString(350, y, "Details")
    y -= 15
    c.line(50, y, 550, y)
    y -= 15
    c.setFont("Helvetica", 12)

    for step in report_data.get('test_steps', []):
        c.drawString(50, y, step['step'])
        c.drawString(250, y, f"■ {step['status']}")
        c.drawString(350, y, step['details'])
        y -= 20

    if 'users_created' in report_data and 'tasks_created' in report_data:
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Data Created During Test:")
        y -= 20
        c.setFont("Helvetica", 12)
        c.drawString(60, y, f"Users Created: {report_data['users_created']}")
        y -= 20
        c.drawString(60, y, f"Tasks Created: {report_data['tasks_created']}")
        y -= 40

    if 'cleanup_steps' in report_data:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Data Cleanup Results:")
        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Operation")
        c.drawString(250, y, "Status")
        c.drawString(350, y, "Details")
        y -= 15
        c.line(50, y, 550, y)
        y -= 15
        c.setFont("Helvetica", 12)

        for op in report_data['cleanup_steps']:
            c.drawString(50, y, op['operation'])
            c.drawString(250, y, f"■ {op['status']}")
            c.drawString(350, y, op['details'])
            y -= 20

    c.save()
    print(f"✅ PDF report generated: {filename}")
    return filename
