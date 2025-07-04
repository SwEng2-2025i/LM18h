from pathlib import Path
from datetime import datetime
from fpdf import FPDF

REPORT_DIR = Path(__file__).parent / "reports"
REPORT_DIR.mkdir(exist_ok=True)

def generate_pdf_report(test_name: str, steps: list[tuple[str, bool, str | None]]):
    """
    steps = [(descripcion, passed_bool, optional_error_string), ...]
    """
    # numera secuencialmente
    n = len(list(REPORT_DIR.glob("report_*.pdf"))) + 1
    pdf_path = REPORT_DIR / f"report_{n:03d}.pdf"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    # pdf.add_page()

    # pdf.set_font("Arial", "B", 14)
    # pdf.cell(0, 10, f"{test_name} – Report #{n}", ln=True)
    # pdf.set_font("Arial", "", 10)
    # pdf.cell(0, 6, f"Date: {datetime.now()}", ln=True)
    # pdf.ln(4)

    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"{test_name} - Report #{n}", ln=True)   

    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"Date: {datetime.now()}", ln=True)
    pdf.ln(4)

    # for desc, ok, err in steps:
    #     status = "✅" if ok else "❌"
    #     line   = f"{status} {desc}"
    #     if err:
    #         line += f" – {err}"
    #     pdf.cell(0, 6, line, ln=True)
    for desc, ok, err in steps:
        status = "[OK]" if ok else "[FAIL]"                  
        line = f"{status} {desc}"
        if err:
            line += f" - {err}"                             
        pdf.cell(0, 6, line, ln=True)

    pdf.output(str(pdf_path))
    print(f"📄 Report saved to {pdf_path}")