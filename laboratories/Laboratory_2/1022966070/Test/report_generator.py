from fpdf import FPDF
import os
from datetime import datetime

class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.test_steps = []
        self.test_result = None
        self.set_font('Arial', '', 12)

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f'Test Report - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def log_step(self, text):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, f"- {text}")
        self.ln(2)
        self.test_steps.append(text)

    def log_test_result(self, success):
        self.set_font('Arial', 'B', 12)
        self.set_y(-40)
        if success:
            self.set_text_color(0, 128, 0)
            self.cell(0, 10, "TEST PASSED", 0, 1, 'L')
        else:
            self.set_text_color(255, 0, 0)
            self.cell(0, 10, "TEST FAILED", 0, 1, 'L')
        self.set_text_color(0, 0, 0)
