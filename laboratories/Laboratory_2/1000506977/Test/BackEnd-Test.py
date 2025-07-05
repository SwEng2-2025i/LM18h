import requests
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    return user_data["id"]

def obtener_usuario_por_id(user_id):
    url_usuario = f"{USERS_URL}/{user_id}"
    response = requests.get(url_usuario)
    return response

def eliminar_usuario_por_id(user_id):
    url_usuario = f"{USERS_URL}/{user_id}"
    response = requests.delete(url_usuario)
    return response

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    return task_data["id"]

def buscar_tarea_por_id(task_id):
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    lista_tareas = response.json()
    
    tarea_encontrada = None
    for tarea in lista_tareas:
        if tarea["id"] == task_id:
            tarea_encontrada = tarea
            break
    
    return tarea_encontrada

def eliminar_tarea_por_id(task_id):
    url_tarea = f"{TASKS_URL}/{task_id}"
    response = requests.delete(url_tarea)
    return response

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    return response.json()

def crear_reporte_backend(lista_resultados):
    nombre_base = "backend_report"
    contador = 1
    
    # Buscar archivo disponible
    while True:
        nombre_archivo = f"{nombre_base}_{contador}.pdf"
        if not os.path.exists(nombre_archivo):
            break
        contador += 1
    
    # Crear documento PDF
    pdf_canvas = canvas.Canvas(nombre_archivo, pagesize=letter)
    ancho, alto = letter
    
    # Título del reporte
    pdf_canvas.setFont("Helvetica-Bold", 16)
    titulo = "Reporte de Pruebas de Integración Backend"
    pdf_canvas.drawString(50, alto - 50, titulo)
    
    # Contenido del reporte
    pdf_canvas.setFont("Helvetica", 12)
    posicion_y = alto - 90
    
    for idx, resultado in enumerate(lista_resultados):
        if posicion_y < 50:  # Nueva página si es necesario
            pdf_canvas.showPage()
            posicion_y = alto - 50
        pdf_canvas.drawString(50, posicion_y, resultado)
        posicion_y -= 20
        
    pdf_canvas.save()
    print(f"Reporte generado: {nombre_archivo}")

def pruebas_integracion_backend():
    lista_resultados = []
    
    # Prueba 1: Crear usuario
    try:
        user_id = create_user("TestUser")
        lista_resultados.append(f"✅ Usuario creado con ID: {user_id}")
    except Exception as error:
        mensaje_error = f"❌ Error al crear usuario: {error}"
        lista_resultados.append(mensaje_error)
        crear_reporte_backend(lista_resultados)
        return

    # Prueba 2: Obtener usuario
    respuesta_usuario = obtener_usuario_por_id(user_id)
    usuario_valido = (respuesta_usuario.status_code == 200 and 
                     respuesta_usuario.json().get("id") == user_id)
    
    if usuario_valido:
        datos_usuario = respuesta_usuario.json()
        lista_resultados.append(f"✅ Usuario obtenido correctamente: {datos_usuario}")
    else:
        lista_resultados.append(f"❌ Error al obtener usuario: {respuesta_usuario.text}")

    # Prueba 3: Crear tarea
    try:
        task_id = create_task(user_id, "Test Task")
        lista_resultados.append(f"✅ Tarea creada con ID: {task_id}")
    except Exception as error:
        mensaje_error = f"❌ Error al crear tarea: {error}"
        lista_resultados.append(mensaje_error)
        # Limpieza antes de salir
        eliminar_usuario_por_id(user_id)
        crear_reporte_backend(lista_resultados)
        return

    # Prueba 4: Obtener tarea
    tarea_encontrada = buscar_tarea_por_id(task_id)
    tarea_valida = tarea_encontrada and tarea_encontrada["id"] == task_id
    
    if tarea_valida:
        lista_resultados.append(f"✅ Tarea obtenida correctamente: {tarea_encontrada}")
    else:
        lista_resultados.append(f"❌ Error al obtener tarea con ID {task_id}")

    # Prueba 5: Eliminar tarea
    respuesta_eliminar_tarea = eliminar_tarea_por_id(task_id)
    eliminacion_exitosa = respuesta_eliminar_tarea.status_code == 200
    
    if eliminacion_exitosa:
        lista_resultados.append(f"✅ Tarea {task_id} eliminada correctamente.")
    else:
        lista_resultados.append(f"❌ Error al eliminar tarea {task_id}: {respuesta_eliminar_tarea.text}")

    # Prueba 6: Verificar eliminación de tarea
    tarea_eliminada = buscar_tarea_por_id(task_id)
    if not tarea_eliminada:
        lista_resultados.append(f"✅ Verificado: la tarea {task_id} ya no existe.")
    else:
        lista_resultados.append(f"❌ Error: la tarea {task_id} aún existe.")

    # Prueba 7: Eliminar usuario
    respuesta_eliminar_usuario = eliminar_usuario_por_id(user_id)
    usuario_eliminado_exitoso = respuesta_eliminar_usuario.status_code == 200
    
    if usuario_eliminado_exitoso:
        lista_resultados.append(f"✅ Usuario {user_id} eliminado correctamente.")
    else:
        lista_resultados.append(f"❌ Error al eliminar usuario {user_id}: {respuesta_eliminar_usuario.text}")

    # Prueba 8: Verificar eliminación de usuario
    respuesta_verificar_usuario = obtener_usuario_por_id(user_id)
    usuario_no_existe = respuesta_verificar_usuario.status_code == 404
    
    if usuario_no_existe:
        lista_resultados.append(f"✅ Verificado: el usuario {user_id} ya no existe.")
    else:
        lista_resultados.append(f"❌ Error: el usuario {user_id} aún existe.")

    crear_reporte_backend(lista_resultados)


if __name__ == "__main__":
    pruebas_integracion_backend()