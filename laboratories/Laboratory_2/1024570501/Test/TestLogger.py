import time
import unicodedata
from datetime import datetime
from fpdf import FPDF
import os

class TestLogger:
    def __init__(self, test_name):
        self.test_name = test_name
        self.start_time = None
        self.end_time = None
        self.logs = []
        self.status = "PASSED"
    
    def start_test(self):
        self.start_time = datetime.now()
        self.add_log("Test started", status="INFO")
    
    def end_test(self):
        self.end_time = datetime.now()
        self.add_log("Test ended", status="INFO")
    
    def add_log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append((timestamp, message, status))
        if status == "FAIL":
            self.status = "FAILED"
    
    def generate_pdf(self):
        if not os.path.exists("reports"):
            os.makedirs("reports")
        
        report_num = 1
        while os.path.exists(f"reports/report_{report_num:03d}.pdf"):
            report_num += 1
        
        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        
        # Use built-in font that supports basic Unicode
        pdf.add_font('Arial', '', r'c:\windows\fonts\arial.ttf', uni=True)  # Windows
        # For Linux/Mac: pdf.add_font('Arial', '', '/Library/Fonts/Arial Unicode.ttf', uni=True)
        pdf.set_font('Arial', '', 12)
        
        # Header
        pdf.cell(200, 10, txt=f"Test Report #{report_num:03d}", ln=True, align='C')
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(200, 10, txt=f"Test Name: {self.test_name}", ln=True, align='L')
        pdf.set_font('Arial', '', 12)
        pdf.cell(200, 10, txt=f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"End Time: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='L')
        duration = self.end_time - self.start_time
        pdf.cell(200, 10, txt=f"Duration: {duration.total_seconds():.2f} seconds", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Status: {self.status}", ln=True, align='L')
        pdf.ln(10)
        
        # Logs header
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(40, 10, "Time", border=1)
        pdf.cell(110, 10, "Message", border=1)
        pdf.cell(40, 10, "Status", border=1, ln=True)
        pdf.set_font('Arial', '', 10)
        
        # Logs content - SAFE UNICODE HANDLING
        for (timestamp, message, status) in self.logs:
            # Normalize Unicode characters to safe equivalents
            safe_message = unicodedata.normalize('NFKD', message).encode('ascii', 'ignore').decode('ascii')
            
            pdf.cell(40, 10, timestamp, border=1)
            pdf.cell(110, 10, safe_message, border=1)
            
            # Use text status instead of symbols
            if status == "PASS":
                status_str = "PASS"
            elif status == "FAIL":
                status_str = "FAIL"
            else:
                status_str = status
                
            pdf.cell(40, 10, status_str, border=1, ln=True)
        
        try:
            pdf.output(f"reports/report_{report_num:03d}.pdf")
        except UnicodeEncodeError:
            # Fallback: Remove all non-ASCII characters
            safe_path = f"reports/report_{report_num:03d}.pdf".encode('ascii', 'ignore').decode('ascii')
            pdf.output(safe_path)
        
        return report_num