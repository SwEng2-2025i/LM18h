import requests
import sys
import io
import os
from LogSaver import Logger, DuplicadorSalida
from reportlab.pdfgen import canvas
import textwrap
# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    Logger.add_to_log("info", "User created: " + str(user_data) +"\n"
                      + "                               Response URL: " + str(response.url) + "\n"
                      + "                               Response StatusCode: " + str(response.status_code) + "\n"
                      + "                               Petition Method: " + str(response.request.method))
    print("✅ User created:", user_data)
    return user_data["id"]

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    Logger.add_to_log("info", "User deleted: " + str(user_id) +"\n"
                      + "                               Response URL: " + str(response.url) + "\n"
                      + "                               Response StatusCode: " + str(response.status_code) + "\n"
                      + "                               Petition Method: " + str(response.request.method))
    print("✅ User deleted:", user_id)
def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    Logger.add_to_log("info", "Task created: " + str(task_data) +"\n"
                      + "                               Response URL: " + str(response.url) + "\n"
                      + "                               Response StatusCode: " + str(response.status_code) + "\n"
                      + "                               Petition Method: " + str(response.request.method))
    print("✅ Task created:", task_data)
    return task_data["id"]

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    Logger.add_to_log("info", "Task deleted: " + str(task_id) +"\n"
                      + "                               Response URL: " + str(response.url) + "\n"
                      + "                               Response StatusCode: " + str(response.status_code) + "\n"
                      + "                               Petition Method: " + str(response.request.method))
    print("✅ Task deleted:", task_id)

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    Logger.add_to_log("info", "Tasks found: " + str(tasks) +"\n"
                      + "                               Response URL: " + str(response.url) + "\n"
                      + "                               Response StatusCode: " + str(response.status_code) + "\n"
                      + "                               Petition Method: " + str(response.request.method))
    return tasks

def get_user_id(user_id):
    response = requests.get(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    Logger.add_to_log("info", "User found: " + str(user_id) +"\n"
                      + "                               Response URL: " + str(response.url) + "\n"
                      + "                               Response StatusCode: " + str(response.status_code) + "\n"
                      + "                               Petition Method: " + str(response.request.method))
    return response.json()
def integration_test():
    # Step 1: Create user
    user_id = create_user("Camilo")

    # Step 2: Create task for that user
    task_id = create_task(user_id, "Prepare presentation")

    # Step 3: Verify that the task is registered and associated with the user
    tasks = get_tasks()
    user_tasks = [t for t in tasks if t["user_id"] == user_id]

    assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
    print("✅ Test completed: task was successfully registered and linked to the user.")
    delete_task(task_id)
    delete_user(user_id)
    print("✅ User and task deleted successfully.")

def limpiar_archivo(nombre_archivo):
    with open(nombre_archivo, "w", encoding="utf-8"):
        pass
def obtener_siguiente_numero(nombre_base="reporteBackEnd", carpeta="reportes", extension=".pdf"):
    os.makedirs(carpeta, exist_ok=True)  # Crea carpeta si no existe
    existentes = [f for f in os.listdir(carpeta) if f.startswith(nombre_base) and f.endswith(extension)]

    numeros = []
    for f in existentes:
        try:
            num = int(f.replace(nombre_base + "_", "").replace(extension, ""))
            numeros.append(num)
        except ValueError:
            pass  # Ignora archivos con nombres no estándar

    siguiente = max(numeros, default=0) + 1
    return os.path.join(carpeta, f"{nombre_base}_{siguiente}{extension}")

def guardar_en_pdf(texto, nombre_pdf):
    c = canvas.Canvas(nombre_pdf)
    y = 800
    margen_izquierdo = 40
    alto_linea = 15

    for linea in texto.split('\n'):
        # Divide la línea si es demasiado larga (wrap)
        sublineas = textwrap.wrap(linea, width=100)
        for sublinea in sublineas:
            c.drawString(margen_izquierdo, y, sublinea)
            y -= alto_linea
            if y < 50:  # Cambia de página si se llega al final
                c.showPage()
                y = 800

    c.save()
def capturar_y_guardar_pdf():

    captura = io.StringIO()
    sys.stdout = DuplicadorSalida(sys.__stdout__, captura)
    limpiar_archivo("Logs/app.log")

    try:
        integration_test()
    finally:
        # Obtener texto de consola
        sys.stdout = sys.__stdout__
        # Obtener texto de logs

    

    with open("Logs/app.log", "r", encoding="utf-8") as f:
        contenido_existente = f.read()
        
    


    # 🔀 Combinar todo (puedes incluir encabezados si quieres)
    contenido_total = (
        "=== SALIDA DE CONSOLA ===\n"
        + captura.getvalue() +
        "\n\n=== LOGS DE PETICIONES ===\n"
        + contenido_existente
    )


    nombre_pdf = obtener_siguiente_numero()
    guardar_en_pdf(contenido_total, nombre_pdf)
    print(f"PDF generado: {nombre_pdf}")
    limpiar_archivo("Logs/app.log")

if __name__ == "__main__":
    capturar_y_guardar_pdf()
#    integration_test()