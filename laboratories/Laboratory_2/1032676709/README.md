# Laboratorio 2 - Pruebas de Integración

## 📋 Descripción

Este laboratorio extiende el ejemplo de pruebas de integración implementado en clase, agregando dos nuevas funcionalidades:

1. **Limpieza de datos (Data cleanup):**  
   Al finalizar las pruebas, todos los datos creados durante su ejecución (usuarios y tareas) se eliminan automáticamente. Además, se verifica que efectivamente hayan sido eliminados.
   
2. **Generación automática de reportes PDF:**  
   Después de ejecutar las pruebas, se genera automáticamente un reporte en formato PDF que contiene los resultados. Los reportes se enumeran secuencialmente (`report_1.pdf`, `report_2.pdf`, ...) y se almacenan en la carpeta `reports/`.

## 🧪 Resultados

Las pruebas se ejecutaron correctamente, creando un usuario y una tarea, verificando su relación y luego eliminando ambos recursos. Los reportes PDF fueron generados automáticamente.

Ejemplo de resultados en un reporte:

✅ Usuario creado con ID: 15
✅ Tarea creada con ID: 17
✅ Asociación tarea-usuario verificada
✅ Tarea 17 eliminada
✅ Usuario 15 eliminado
✅ Verificación de limpieza exitosa

# 🔧 Servicios y código modificado

- `Test/BackEnd-Test.py`
  - Se agregó la función `delete_task()` y `delete_user()` para limpiar los datos creados.
  - Se añadió lógica en el bloque `finally:` para eliminar y verificar la eliminación de datos.
  - Se integró la función `generate_pdf_report()` para generar el PDF de resultados.

- `Test/FrontEnd-Test.py`
  - Se mejoró la extracción del ID de la tarea desde la interfaz web.
  - Se agregó almacenamiento y limpieza de datos creados durante el test.
  - Se añadió la generación automática de reporte PDF al final de las pruebas.

- `Test/generate_report.py`
  - Nuevo módulo que genera reportes PDF secuenciales dentro del directorio `reports/`.

- `Users_Service/main.py`
  - ✅ Se agregó la ruta `DELETE /users/<int:user_id>` para poder eliminar usuarios.

```
@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    db.session.delete(user)
    db.session.commit()
    return '', 204
```

- `Task_Service/main.py`
  - ✅ Se agregó la ruta `DELETE /tasks/<int:task_id>` para poder eliminar usuarios.

```
@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    db.session.delete(task)
    db.session.commit()
    return '', 204
```

## 📁 Estructura del repositorio

Laboratory_2/
├── 1032676709/
│   ├── Front-End/
│   ├── Task_Service/
│   │   ├── instance/
│   │   └── main.py
│   ├── Users_Service/
│   │   ├── instance/
│   │   └── main.py
│   ├── Test/
│   │   ├── reports/
│   │   ├── BackEnd-Test.py
│   │   ├── FrontEnd-Test.py
│   │   └── generate_report.py
│   ├──README.md
│   └──requirements.txt

## ✅ Estado

✔️ Todos los requerimientos del laboratorio han sido implementados satisfactoriamente.  
✔️ Las pruebas automatizadas limpian sus datos.  
✔️ Los reportes PDF se generan correctamente sin sobrescribir los anteriores.