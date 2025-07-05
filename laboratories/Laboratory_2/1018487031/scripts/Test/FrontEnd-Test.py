import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import requests

class FrontEndTestRunner:
    def __init__(self):
        self.test_results = []
        self.created_users = []
        self.created_tasks = []
        self.start_time = None
        self.end_time = None
        self.driver = None

    def log_result(self, test_name, status, message=""):
        """Función de test de loggeo para el reporte de pdf"""
        self.test_results.append({
            'test': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
        print(f"{'✅' if status == 'PASS' else '❌'} {test_name}: {message}")

    def setup_driver(self):
        """Función para inicializar Chrome WebDriver"""
        try:
            options = Options()
            # options.add_argument('--headless')  # Quitar comentario para modo headless 
            self.driver = webdriver.Chrome(options=options)
            self.log_result("Driver Setup", "PASS", "Chrome WebDriver initialized")
            return True
        except Exception as e:
            self.log_result("Driver Setup", "FAIL", f"Failed to initialize driver: {str(e)}")
            return False

    def abrir_frontend(self):
        """Función para abrir el frontend en el navegador"""
        try:
            self.driver.get("http://localhost:5000")
            time.sleep(2)
            self.log_result("Open Frontend", "PASS", "Frontend application loaded")
            return True
        except Exception as e:
            self.log_result("Open Frontend", "FAIL", f"Failed to load frontend: {str(e)}")
            return False

    def crear_usuario(self, wait, username="Ana"):
        """Función que crea el usuario a traves del frontend y genera trazabilidad para la limpieza"""
        try:
            username_input = self.driver.find_element(By.ID, "username")
            username_input.clear()
            username_input.send_keys(username)
            time.sleep(1)
            
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
            time.sleep(2)

            user_result = self.driver.find_element(By.ID, "user-result").text
            
            if "Usuario creado con ID" in user_result:
                user_id = ''.join(filter(str.isdigit, user_result))
                self.created_users.append(int(user_id))
                self.log_result("Create User via Frontend", "PASS", 
                              f"User '{username}' created with ID {user_id}")
                return user_id
            else:
                self.log_result("Create User via Frontend", "FAIL", 
                              f"User creation failed: {user_result}")
                return None
        except Exception as e:
            self.log_result("Create User via Frontend", "FAIL", f"Error creating user: {str(e)}")
            return None

    def crear_tarea(self, wait, user_id, task_title="Terminar laboratorio"):
        """Función que crea la tarea a traves del frontend y genera trazabilidad para la limpieza"""
        try:
            task_input = self.driver.find_element(By.ID, "task")
            task_input.clear()
            task_input.send_keys(task_title)
            time.sleep(1)

            userid_input = self.driver.find_element(By.ID, "userid")
            userid_input.clear()
            userid_input.send_keys(user_id)
            time.sleep(1)

            crear_tarea_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
            )
            crear_tarea_btn.click()
            time.sleep(2)

            wait.until(
                EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
            )
            task_result = self.driver.find_element(By.ID, "task-result").text
            
            if "Tarea creada con ID" in task_result:
                task_id = ''.join(filter(str.isdigit, task_result))
                self.created_tasks.append(int(task_id))
                self.log_result("Create Task via Frontend", "PASS", 
                              f"Task '{task_title}' created with ID {task_id}")
                return task_id
            else:
                self.log_result("Create Task via Frontend", "FAIL", 
                              f"Task creation failed: {task_result}")
                return None
        except Exception as e:
            self.log_result("Create Task via Frontend", "FAIL", f"Error creating task: {str(e)}")
            return None

    def ver_tareas(self, expected_task="Terminar laboratorio"):
        """Función que verifica que las tareas se muestren correctamente"""
        try:
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
            time.sleep(2)

            tasks = self.driver.find_element(By.ID, "tasks").text
            
            if expected_task in tasks:
                self.log_result("View Tasks", "PASS", f"Task '{expected_task}' found in task list")
                return True
            else:
                self.log_result("View Tasks", "FAIL", f"Task '{expected_task}' not found in task list")
                return False
        except Exception as e:
            self.log_result("View Tasks", "FAIL", f"Error viewing tasks: {str(e)}")
            return False

    def cleanup_test_data(self):
        """Función que limpia los datos de prueba lo mediante llamados API DELETE"""
        cleanup_success = True
        
        # Limpia las tareas (debido a las restricciones de llave foránea)
        for task_id in self.created_tasks:
            try:
                response = requests.delete(f"http://localhost:5002/tasks/{task_id}")
                if response.status_code in [200, 404]:  # 200 = deleted, 404 = already gone
                    self.log_result("Cleanup Task", "PASS", f"Task {task_id} deleted successfully")
                else:
                    self.log_result("Cleanup Task", "FAIL", f"Failed to delete task {task_id}: {response.text}")
                    cleanup_success = False
            except Exception as e:
                self.log_result("Cleanup Task", "FAIL", f"Failed to cleanup task {task_id}: {str(e)}")
                cleanup_success = False
        
        # Limpia los usuarios después de limpiar las tareas
        for user_id in self.created_users:
            try:
                response = requests.delete(f"http://localhost:5001/users/{user_id}")
                if response.status_code in [200, 404]:  
                    self.log_result("Cleanup User", "PASS", f"User {user_id} deleted successfully")
                else:
                    self.log_result("Cleanup User", "FAIL", f"Failed to delete user {user_id}: {response.text}")
                    cleanup_success = False
            except Exception as e:
                self.log_result("Cleanup User", "FAIL", f"Failed to cleanup user {user_id}: {str(e)}")
                cleanup_success = False
        
        return cleanup_success

    def verify_cleanup(self):
        """Función que verifica que los datos se borraron correctamente"""
        verification_passed = True
        
        # Verifica que las tareas hayan sido borradas
        try:
            response = requests.get("http://localhost:5002/tasks")
            if response.status_code == 200:
                current_tasks = response.json()
                remaining_test_tasks = [t for t in current_tasks if t['id'] in self.created_tasks]
                
                if remaining_test_tasks:
                    self.log_result("Verify Task Cleanup", "FAIL", 
                                  f"Found {len(remaining_test_tasks)} tasks that should have been deleted")
                    verification_passed = False
                else:
                    self.log_result("Verify Task Cleanup", "PASS", "All test tasks properly cleaned up")
            else:
                self.log_result("Verify Task Cleanup", "FAIL", "Could not verify task cleanup")
                verification_passed = False
        except Exception as e:
            self.log_result("Verify Task Cleanup", "FAIL", f"Error verifying task cleanup: {str(e)}")
            verification_passed = False
        
         # Verifica que los usuarios han sido borrados
        for user_id in self.created_users:
            try:
                response = requests.get(f"http://localhost:5001/users/{user_id}")
                if response.status_code == 200:
                    self.log_result("Verify User Cleanup", "FAIL", f"User {user_id} still exists")
                    verification_passed = False
                else:
                    self.log_result("Verify User Cleanup", "PASS", f"User {user_id} properly cleaned up")
            except Exception as e:
                self.log_result("Verify User Cleanup", "FAIL", f"Error verifying user {user_id}: {str(e)}")
                verification_passed = False
        
        return verification_passed

    def generate_pdf_report(self):
        """Función para generar reporte PDF"""
        # Crea un directorio de reportes si no existe
        os.makedirs("reports", exist_ok=True)
        
        # Encuentra el siguiente número de reporte de forma secuencial
        existing_reports = [f for f in os.listdir("reports") if f.startswith("frontend_test_report_") and f.endswith(".pdf")]
        if existing_reports:
            numbers = []
            for report in existing_reports:
                try:
                    num = int(report.split("_")[-1].split(".")[0])
                    numbers.append(num)
                except:
                    continue
            next_num = max(numbers) + 1 if numbers else 1
        else:
            next_num = 1
        
        filename = f"reports/frontend_test_report_{next_num:03d}.pdf"
        
        # Crear PDF
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Título del PDF
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  
        )
        story.append(Paragraph("Frontend E2E Test Report", title_style))
        story.append(Spacer(1, 20))
        
        # # Información del test
        info_style = styles['Normal']
        story.append(Paragraph(f"<b>Test Execution Date:</b> {datetime.now().strftime('%Y-%m-%d')}", info_style))
        story.append(Paragraph(f"<b>Start Time:</b> {self.start_time}", info_style))
        story.append(Paragraph(f"<b>End Time:</b> {self.end_time}", info_style))
        story.append(Paragraph(f"<b>Report Number:</b> {next_num:03d}", info_style))
        story.append(Spacer(1, 20))
        
        # Resumen de los resultados del test
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = total_tests - passed_tests
        
        story.append(Paragraph("<b>Test Summary:</b>", styles['Heading2']))
        story.append(Paragraph(f"Total Tests: {total_tests}", info_style))
        story.append(Paragraph(f"Passed: {passed_tests}", info_style))
        story.append(Paragraph(f"Failed: {failed_tests}", info_style))
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("<b>Test Data Created:</b>", styles['Heading2']))
        story.append(Paragraph(f"Users Created: {len(self.created_users)} {self.created_users}", info_style))
        story.append(Paragraph(f"Tasks Created: {len(self.created_tasks)} {self.created_tasks}", info_style))
        story.append(Spacer(1, 20))
        
        # Resultados detallados
        story.append(Paragraph("<b>Detailed Results:</b>", styles['Heading2']))
        for result in self.test_results:
            status_color = "green" if result['status'] == 'PASS' else "red"
            story.append(Paragraph(
                f"<font color='{status_color}'>[{result['status']}]</font> "
                f"<b>{result['test']}</b> ({result['timestamp']})", 
                info_style
            ))
            if result['message']:
                story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{result['message']}", info_style))
            story.append(Spacer(1, 10))
        
        doc.build(story)
        self.log_result("PDF Report", "PASS", f"Report generated: {filename}")
        return filename

    def run_full_test(self):
        """Función que corre el E2E test suite junto con la limpieza y el reporte de pruebas"""
        self.start_time = datetime.now().strftime("%H:%M:%S")
        print("🚀 Starting Frontend E2E Test Suite...")
        
        try:
            if not self.setup_driver():
                return False
            
            wait = WebDriverWait(self.driver, 10)
            
            
            if not self.abrir_frontend():
                return False
            
            user_id = self.crear_usuario(wait)
            if not user_id:
                return False
            
            task_id = self.crear_tarea(wait, user_id)
            if not task_id:
                return False
            
            if not self.ver_tareas():
                return False
            
            # Mensaje de limpieza de datos
            print("\n🧹 Cleaning up test data...")
            cleanup_success = self.cleanup_test_data()
            
            # Mensaje de verificación de limpieza
            print("🔍 Verifying data cleanup...")
            verification_passed = self.verify_cleanup()
            
            self.end_time = datetime.now().strftime("%H:%M:%S")
            
            # Mensaje de generación de reporte PDF
            print("\n📄 Generating PDF report...")
            report_file = self.generate_pdf_report()
            
            # Mensaje de los resultados del test
            print(f"\n📊 Test Suite Complete!")
            print(f"E2E Test Flow: PASSED")
            print(f"Data Cleanup: {'PASSED' if cleanup_success else 'FAILED'}")
            print(f"Cleanup Verification: {'PASSED' if verification_passed else 'FAILED'}")
            print(f"PDF Report: {report_file}")
            
            return cleanup_success and verification_passed
            
        except Exception as e:
            self.end_time = datetime.now().strftime("%H:%M:%S")
            self.log_result("Test Suite", "FAIL", f"Test suite failed: {str(e)}")
            if hasattr(self, 'driver') and self.driver:
                self.generate_pdf_report()
            return False
        finally:
            if self.driver:
                time.sleep(3)  # Tiempo de delay para poder observar los resultados en la pestaña del navegador
                self.driver.quit()

if __name__ == "__main__":
    runner = FrontEndTestRunner()
    success = runner.run_full_test()
    exit(0 if success else 1)
