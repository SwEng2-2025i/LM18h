import requests
from pdf_generator import TestReportGenerator

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ Usuario creado:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Tarea creada:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def delete_user(user_id):
    """Eliminar un usuario por ID"""
    response = requests.delete(f"{USERS_URL}/{user_id}")
    if response.status_code == 200:
        print(f"✅ Usuario {user_id} eliminado exitosamente")
        return True
    else:
        print(f"❌ Error al eliminar usuario {user_id}: {response.status_code}")
        return False

def delete_task(task_id):
    """Eliminar una tarea por ID"""
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    if response.status_code == 200:
        print(f"✅ Tarea {task_id} eliminada exitosamente")
        return True
    else:
        print(f"❌ Error al eliminar tarea {task_id}: {response.status_code}")
        return False

def verify_user_deleted(user_id):
    """Verificar que un usuario ha sido eliminado"""
    try:
        response = requests.get(f"{USERS_URL}/{user_id}")
        if response.status_code == 404:
            print(f"✅ Usuario {user_id} verificado como eliminado")
            return True
        else:
            print(f"❌ Usuario {user_id} aún existe (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Error al verificar usuario {user_id}: {str(e)}")
        return False

def verify_task_deleted(task_id):
    """Verificar que una tarea ha sido eliminada"""
    try:
        # Primero intentar con el endpoint específico
        response = requests.get(f"{TASKS_URL}/{task_id}")
        if response.status_code == 404:
            print(f"✅ Tarea {task_id} verificada como eliminada")
            return True
        elif response.status_code == 405:
            # Si el endpoint específico no funciona, usar el endpoint de listar todas
            print(f"⚠️ Endpoint específico no disponible, verificando con lista completa...")
            all_tasks = get_tasks()
            task_exists = any(task['id'] == task_id for task in all_tasks)
            if not task_exists:
                print(f"✅ Tarea {task_id} verificada como eliminada (usando lista completa)")
                return True
            else:
                print(f"❌ Tarea {task_id} aún existe en la lista")
                return False
        else:
            print(f"❌ Tarea {task_id} aún existe (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Error al verificar tarea {task_id}: {str(e)}")
        return False

def integration_test():
    test_results = {
        'status': 'PASS',
        'user_id': None,
        'task_id': None,
        'user_created': False,
        'task_created': False,
        'user_deleted': False,
        'task_deleted': False,
        'cleanup_verified': False
    }
    
    try:
        # Paso 1: Crear usuario
        user_id = create_user("Camilo")
        test_results['user_id'] = user_id
        test_results['user_created'] = True

        # Paso 2: Crear tarea para ese usuario
        task_id = create_task(user_id, "Preparar presentación")
        test_results['task_id'] = task_id
        test_results['task_created'] = True

        # Paso 3: Verificar que la tarea está registrada y asociada con el usuario
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]

        assert any(t["id"] == task_id for t in user_tasks), "❌ La tarea no fue registrada correctamente"
        print("✅ Prueba completada: la tarea fue registrada exitosamente y vinculada al usuario.")

        # Paso 4: Limpieza - Eliminar los datos creados
        print("\n🧹 Iniciando proceso de limpieza...")
        
        # Eliminar tarea primero (para evitar problemas de clave foránea)
        if delete_task(task_id):
            test_results['task_deleted'] = True
        
        # Eliminar usuario
        if delete_user(user_id):
            test_results['user_deleted'] = True
        
        # Paso 5: Verificar limpieza
        print("\n🔍 Verificando limpieza...")
        user_deleted = verify_user_deleted(user_id)
        task_deleted = verify_task_deleted(task_id)
        
        if user_deleted and task_deleted:
            print("✅ Verificación de limpieza exitosa: Todos los datos de prueba han sido eliminados correctamente")
            test_results['cleanup_verified'] = True
        else:
            print("❌ Verificación de limpieza falló: Algunos datos de prueba permanecen")
            test_results['status'] = 'FAIL'
            test_results['cleanup_verified'] = False

    except Exception as e:
        print(f"❌ La prueba falló con error: {str(e)}")
        test_results['status'] = 'FAIL'
        test_results['error'] = str(e)
    
    # Generar reporte PDF
    print("\n📄 Generando reporte PDF...")
    generator = TestReportGenerator("Backend")
    generator.generate_report(test_results)
    
    return test_results

if __name__ == "__main__":
    integration_test()