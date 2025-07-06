from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def generate_report(dir, resultados, titulo, nombre):
    w, h = letter
    num_files = len(os.listdir(dir))

    c = canvas.Canvas(f"{dir}/{nombre}_{num_files + 1}.pdf", pagesize=letter)
    c.setFont("Helvetica", size=20)
    c.drawString(30, h - 50, f"{titulo} # {num_files + 1}")

    y = 700
    x = 50
    counter = 1

    for i in resultados:
        c.setFont("Helvetica", 13)
        c.drawString(x, y, f"{counter}. Descripción del test: {i["descripcion"]}")
        y -= 15
        c.setFont("Helvetica", 10)
        c.drawString(x + 30, y, f"Resultado del test: {"Test superado" if i["resultado"] == True else "Test fallido"}")
        y -= 30
        counter += 1
    c.save()


