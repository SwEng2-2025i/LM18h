from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_pdf_report(lines):
    os.makedirs("reports", exist_ok=True)
    
    existing = [
        int(f.split('_')[1].split('.')[0])
        for f in os.listdir("reports")
        if f.startswith("report_") and f.endswith(".pdf")
    ]
    next_id = max(existing) + 1 if existing else 1
    filename = f"reports/report_{next_id}.pdf"

    c = canvas.Canvas(filename)
    c.setFont("Helvetica", 12)
    c.drawString(100, 800, f"Test Report #{next_id}")
    c.drawString(100, 785, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    y = 750
    for line in lines:
        c.drawString(100, y, line)
        y -= 20

    c.save()
    print(f"✅ Reporte generado: {filename}")