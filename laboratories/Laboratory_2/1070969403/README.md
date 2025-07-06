
# Informe de Resultados

Los dos scripts de prueba han sido extendidos [`BackEnd-Test.py` `FrontEnd-Test.py`]

- **Limpieza de datos:**
  - Todos los datos (usuario y tarea) creados por la prueba se eliminan al finalizar.
  - El script verifica que los datos hayan sido eliminados correctamente.
- **Generación automática de reporte PDF:**
  - Después de cada ejecución, se genera un reporte PDF en la carpeta `reports`.
  - Cada reporte tiene un número secuencial y los anteriores se conservan.

- **Se crea un nuevo archivo que automatiza la ejecucion de las dos pruebas de manera consecutiva:**
  - Basta con solo ejecutar este archivo `test.py`


# Instrucciones

### - Crear y activar un entorno virtual 

```powershell
python -m venv venv
./venv/Scripts/Activate
```

### - Instalar dependencias
```powershell
pip install -r requirements.txt
```

### - Ejecutar los servicios requeridos

Por cada servicio abrir una nueva terminal con nuestro ambiente:

```powershell
./venv/Scripts/Activate
```
Y luego el servicio que queremos:
  ```powershell
  cd "Users_Service"
  python main.py
  ```
  ```powershell
  cd "Task_Service"
  python main.py
  ```
  ```powershell
  cd "Front-End"
  python main.py
  ```

### - Finalmente las pruebas de integración

```powershell
./venv/Scripts/Activate
```
```powershell
cd Test
python tests.py
```

# Output

```
============================================================
🚀 Running Backend Integration Tests
============================================================
 User created: {'id': 17, 'name': 'Camilo'}
 Task created: {'id': 2, 'title': 'Prepare presentation', 'user_id': 17}
 Task 2 deleted.
 User 17 deleted.
PDF report generated: \report_6.pdf
 Data cleanup verified.

✅ Backend Integration Tests completed successfully

============================================================
🚀 Running Frontend E2E Tests
============================================================

DevTools listening on ws://127.0.0.1:53038/devtools/browser/ab961e08-601b-47cd-88a8-c99e575e66f5
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1751771416.606375   28844 voice_transcription.cc:58] Registering VoiceTranscriptionCapability
[28280:26340:0705/221016.951:ERROR:google_apis\gcm\engine\registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
[28280:26340:0705/221017.061:ERROR:google_apis\gcm\engine\mcs_client.cc:700]   Error code: 401  Error message: Authentication Failed: wrong_secret
[28280:26340:0705/221017.061:ERROR:google_apis\gcm\engine\mcs_client.cc:702] Failed to log in to GCM, resetting connection.
Created TensorFlow Lite XNNPACK delegate for CPU.
Attempting to use a delegate that only supports static-sized tensors with a graph that has dynamic-sized tensors (tensor#-1 is a dynamic-sized tensor).
Resultado usuario:
Texto en task_result:
Tareas: Terminar laboratorio (Usuario ID: 17)
Terminar laboratorio (Usuario ID: 17)
PDF report generated: \report_7.pdf
Data cleanup verified.

✅ Frontend E2E Tests completed successfully
```