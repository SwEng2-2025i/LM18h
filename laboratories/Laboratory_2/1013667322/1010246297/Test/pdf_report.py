import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf_report(content, report_title="Integration Test Report", file_prefix="report"):
    reports_dir = os.path.join(os.path.dirname(__file__), "test_reports")
    os.makedirs(reports_dir, exist_ok=True)
    existing = [f for f in os.listdir(reports_dir) if f.startswith(file_prefix) and f.endswith(".pdf")]
    next_num = 1 + max([int(f.rsplit("_", 1)[1].split(".")[0]) for f in existing] or [0])
    filename = os.path.join(reports_dir, f"{file_prefix}_{next_num}.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, f"{report_title} #{next_num}")

   
    c.setFont("Helvetica", 10)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(50, height - 70, f"Generated: {now}")

    
    c.setLineWidth(1)
    c.line(50, height - 80, width - 50, height - 80)

    c.setFont("Helvetica", 12)
    y = height - 110
    if isinstance(content, str):
        lines = content.splitlines()
    else:
        lines = content
    for line in lines:
        if y < 60:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 12)
        c.drawString(60, y, line)
        y -= 18

    c.save()
    print(f"✅ PDF report generated: {filename}")