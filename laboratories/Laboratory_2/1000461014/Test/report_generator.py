import os
from datetime import datetime
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

def generate_pdf_report(log, status, prefix):
    reports_dir = f"reports/{prefix}"
    os.makedirs(reports_dir, exist_ok=True)

    existing_reports = [f for f in os.listdir(reports_dir) if f.startswith(f"{prefix}_report_") and f.endswith(".pdf")]
    next_number = len(existing_reports) + 1
    file_path = os.path.join(reports_dir, f"{prefix}_report_{next_number}.pdf")

    c = canvas.Canvas(file_path, pagesize=LETTER)
    width, height = LETTER

    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, height - inch, f"{prefix.capitalize()} Integration Test Report {next_number}")

    c.setFont("Helvetica", 10)
    c.drawString(inch, height - 1.25 * inch, f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(inch, height - 1.45 * inch, f"Status: {status}")
    c.line(inch, height - 1.6 * inch, width - inch, height - 1.6 * inch)

    text = c.beginText(inch, height - 1.8 * inch)
    text.setFont("Courier", 9)
    
    for line in log:
        text.textLine(line)

        if text.getY() < 1.5 * inch:
            c.drawText(text)
            c.showPage()
            text = c.beginText(inch, height - inch)
            text.setFont("Courier", 9)

    c.drawText(text)
    c.save()
    print(f"\n{prefix.capitalize()} Report saved as: {file_path}")