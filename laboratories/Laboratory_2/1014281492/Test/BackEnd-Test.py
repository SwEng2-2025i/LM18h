import requests
from pdf_report_generator import GeneradorReportePDF

# Endpoints
USUARIOS_URL = "http://localhost:5001/usuarios"
TAREAS_URL = "http://localhost:5002/tareas"

def crear_usuario(nombre):
    response = requests.post(USUARIOS_URL, json={"nombre": nombre})
    response.raise_for_status()
    datos_usuario = response.json()
    print("✅ Usuario creado:", datos_usuario)
    return datos_usuario["id"]

def crear_tarea(usuario_id, descripcion):
    response = requests.post(TAREAS_URL, json={
        "titulo": descripcion,
        "usuario_id": usuario_id
    })
    response.raise_for_status()
    datos_tarea = response.json()
    print("✅ Tarea creada:", datos_tarea)
    return datos_tarea["id"]

def obtener_tareas():
    response = requests.get(TAREAS_URL)
    response.raise_for_status()
    tareas = response.json()
    return tareas

def eliminar_usuario(usuario_id):
    response = requests.delete(f"{USUARIOS_URL}/{usuario_id}")
    response.raise_for_status()
    print(f"✅ Usuario {usuario_id} eliminado.")

def eliminar_tarea(tarea_id):
    response = requests.delete(f"{TAREAS_URL}/{tarea_id}")
    response.raise_for_status()
    print(f"✅ Tarea {tarea_id} eliminada.")

def obtener_usuario(usuario_id):
    response = requests.get(f"{USUARIOS_URL}/{usuario_id}")
    return response

def obtener_tarea(tarea_id):
    response = requests.get(f"{TAREAS_URL}/{tarea_id}")
    return response

def prueba_integracion():
    reporte = GeneradorReportePDF("Reporte de Prueba de Integración Backend")
    usuario_id = None
    tarea_id = None
    try:
        # Paso 1: Crear usuario
        usuario_id = crear_usuario("Camilo")
        reporte.agregar_linea(f"Usuario creado con ID: {usuario_id}")

        # Paso 2: Crear tarea para ese usuario
        tarea_id = crear_tarea(usuario_id, "Preparar presentación")
        reporte.agregar_linea(f"Tarea creada con ID: {tarea_id}")

        # Paso 3: Verificar que la tarea está registrada y asociada con el usuario
        tareas = obtener_tareas()
        tareas_usuario = [t for t in tareas if t["usuario_id"] == usuario_id]

        assert any(t["id"] == tarea_id for t in tareas_usuario), "❌ La tarea no fue registrada correctamente"
        print("✅ Prueba completada: la tarea fue registrada exitosamente y vinculada al usuario.")
        reporte.agregar_linea("Prueba completada: la tarea fue registrada exitosamente y vinculada al usuario.")

    finally:
        if tarea_id:
            eliminar_tarea(tarea_id)
            reporte.agregar_linea(f"Tarea {tarea_id} eliminada.")
            # Verificar eliminación de tarea
            response = obtener_tarea(tarea_id)
            assert response.status_code == 404, f"❌ La tarea {tarea_id} no fue eliminada correctamente."
            reporte.agregar_linea(f"Verificada eliminación de tarea {tarea_id}.")

        if usuario_id:
            eliminar_usuario(usuario_id)
            reporte.agregar_linea(f"Usuario {usuario_id} eliminado.")
            # Verificar eliminación de usuario
            response = obtener_usuario(usuario_id)
            assert response.status_code == 404, f"❌ El usuario {usuario_id} no fue eliminado correctamente."
            reporte.agregar_linea(f"Verificada eliminación de usuario {usuario_id}.")
        
        reporte.generar("reportes")
        print("✅ Reporte PDF generado.")


if __name__ == "__main__":
    prueba_integracion()