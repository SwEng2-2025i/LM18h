from fpdf import FPDF
import os

class PDFReportGenerator:
    def __init__(self, description):
        self.description = description
        self.report_lines = []

    def add_line(self, line):
        self.report_lines.append(line)

    def generate(self, folder="reports"):
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        files = os.listdir(folder)
        report_num = 1
        while f"report_{report_num}.pdf" in files:
            report_num += 1
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt=self.description, ln=True, align='C')
        
        for line in self.report_lines:
            pdf.multi_cell(0, 10, txt=line)
            
        pdf.output(os.path.join(folder, f"report_{report_num}.pdf"))
