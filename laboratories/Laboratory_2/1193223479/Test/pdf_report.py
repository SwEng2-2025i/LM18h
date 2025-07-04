from datetime import datetime
import os
from reportlab.pdfgen import canvas

def pdf_report(sections):
    os.makedirs("report", exist_ok=True)

    exists = [
        int(f.split('_')[1].split('.')[0])
        for f in os.listdir("report")
        if f.startswith("report_") and f.endswith(".pdf")
    ]
    next = max(exists) + 1 if exists else 1
    rep_name = f"report/report_{next}.pdf"

    canv = canvas.Canvas(rep_name)
    canv.setFont("Times-Roman", 12)
    canv.drawString(100, 800, f"Test Report No. {next}")
    canv.drawString(100, 750, f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    y= 700
    for section in sections:
        canv.drawString(100, y, section)
        y -= 20

    canv.save()
    print("PDF Report Generated")

