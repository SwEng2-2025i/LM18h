import requests
import json
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

class BackEndTestRunner:
    def __init__(self):
        self.created_users = []
        self.created_tasks = []
        self.test_results = []
        self.start_time = None
        self.end_time = None

    def log_result(self, test_name, status, message=""):
        """Función de test de loggeo para el reporte de pdf"""
        self.test_results.append({
            'test': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
        print(f"{'✅' if status == 'PASS' else '❌'} {test_name}: {message}")

    def create_user(self, name):
        """Función para crear usuario y generar trazabilidad para la limpieza"""
        try:
            response = requests.post(USERS_URL, json={"name": name})
            response.raise_for_status()
            user_data = response.json()
            self.created_users.append(user_data["id"])
            self.log_result("Create User", "PASS", f"User '{name}' created with ID {user_data['id']}")
            return user_data["id"]
        except Exception as e:
            self.log_result("Create User", "FAIL", f"Failed to create user: {str(e)}")
            raise

    def create_task(self, user_id, description):
        """Función para crear tarea y generar trazabilidad para la limpieza"""
        try:
            response = requests.post(TASKS_URL, json={
                "title": description,
                "user_id": user_id
            })
            response.raise_for_status()
            task_data = response.json()
            self.created_tasks.append(task_data["id"])
            self.log_result("Create Task", "PASS", f"Task '{description}' created with ID {task_data['id']}")
            return task_data["id"]
        except Exception as e:
            self.log_result("Create Task", "FAIL", f"Failed to create task: {str(e)}")
            raise

    def get_tasks(self):
        """Lectura de tareas"""
        try:
            response = requests.get(TASKS_URL)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log_result("Get Tasks", "FAIL", f"Failed to get tasks: {str(e)}")
            raise

    def delete_user(self, user_id):
        """Función para borrar usuario"""
        try:
            response = requests.delete(f"{USERS_URL}/{user_id}")
            if response.status_code == 200:
                self.log_result("Delete User", "PASS", f"User {user_id} deleted successfully")
                return True
            elif response.status_code == 404:
                self.log_result("Delete User", "PASS", f"User {user_id} not found (already deleted)")
                return True
            else:
                self.log_result("Delete User", "FAIL", f"Failed to delete user {user_id}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Delete User", "FAIL", f"Error deleting user {user_id}: {str(e)}")
            return False

    def delete_task(self, task_id):
        """Función para borrar tarea"""
        try:
            response = requests.delete(f"{TASKS_URL}/{task_id}")
            if response.status_code == 200:
                self.log_result("Delete Task", "PASS", f"Task {task_id} deleted successfully")
                return True
            elif response.status_code == 404:
                self.log_result("Delete Task", "PASS", f"Task {task_id} not found (already deleted)")
                return True
            else:
                self.log_result("Delete Task", "FAIL", f"Failed to delete task {task_id}: {response.text}")
                return False
        except Exception as e:
            self.log_result("Delete Task", "FAIL", f"Error deleting task {task_id}: {str(e)}")
            return False

    def cleanup_test_data(self):
        """Función para borrar los datos durante el tests"""
        cleanup_success = True
        
        # Borrar tareas
        for task_id in self.created_tasks:
            if not self.delete_task(task_id):
                cleanup_success = False
        
        # Borrar usuarios
        for user_id in self.created_users:
            if not self.delete_user(user_id):
                cleanup_success = False
        
        return cleanup_success

    def verify_cleanup(self):
        """Función para verificar que los datos se borraron correctamente"""
        verification_passed = True
        
        # Verifica que las tareas hayan sido borradas
        try:
            current_tasks = self.get_tasks()
            remaining_test_tasks = [t for t in current_tasks if t['id'] in self.created_tasks]
            
            if remaining_test_tasks:
                self.log_result("Verify Task Cleanup", "FAIL", 
                              f"Found {len(remaining_test_tasks)} tasks that should have been deleted: {[t['id'] for t in remaining_test_tasks]}")
                verification_passed = False
            else:
                self.log_result("Verify Task Cleanup", "PASS", "All test tasks properly cleaned up")
        except Exception as e:
            self.log_result("Verify Task Cleanup", "FAIL", f"Error verifying task cleanup: {str(e)}")
            verification_passed = False
        
        # Verifica que los usuarios han sido borrados
        for user_id in self.created_users:
            try:
                response = requests.get(f"{USERS_URL}/{user_id}")
                if response.status_code == 200:
                    self.log_result("Verify User Cleanup", "FAIL", f"User {user_id} still exists after cleanup")
                    verification_passed = False
                elif response.status_code == 404:
                    self.log_result("Verify User Cleanup", "PASS", f"User {user_id} properly cleaned up")
                else:
                    self.log_result("Verify User Cleanup", "FAIL", f"Unexpected response for user {user_id}: {response.status_code}")
                    verification_passed = False
            except Exception as e:
                self.log_result("Verify User Cleanup", "FAIL", f"Error verifying user {user_id}: {str(e)}")
                verification_passed = False
        
        return verification_passed

    def integration_test(self):
        """Test de integración principal y limpieza"""
        try:
            # Paso 1: Crear Usuario
            user_id = self.create_user("Camilo")

            # Paso 2: Crear tarea para dicho usuario
            task_id = self.create_task(user_id, "Prepare presentation")

            # Paso 3: Verificar que la tarea está registrada y asociada con el usuario
            tasks = self.get_tasks()
            user_tasks = [t for t in tasks if t["user_id"] == user_id]

            if any(t["id"] == task_id for t in user_tasks):
                self.log_result("Integration Test", "PASS", 
                              "Task successfully registered and linked to user")
            else:
                self.log_result("Integration Test", "FAIL", 
                              "Task was not correctly registered")
                return False

            return True

        except Exception as e:
            self.log_result("Integration Test", "FAIL", f"Test failed with error: {str(e)}")
            return False

    def generate_pdf_report(self):
        """Función para generar reporte PDF"""
        # Crea un directorio de reportes si no existe
        os.makedirs("reports", exist_ok=True)
        
        # Encuentra el siguiente número de reporte de forma secuencial
        existing_reports = [f for f in os.listdir("reports") if f.startswith("backend_test_report_") and f.endswith(".pdf")]
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
        
        filename = f"reports/backend_test_report_{next_num:03d}.pdf"
        
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
        story.append(Paragraph("Backend Integration Test Report", title_style))
        story.append(Spacer(1, 20))
        
        # Información del test
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
        
        # Resumen de los datos del test
        story.append(Paragraph("<b>Test Data Summary:</b>", styles['Heading2']))
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
        """Run complete test suite with cleanup and reporting"""
        self.start_time = datetime.now().strftime("%H:%M:%S")
        print("🚀 Starting Backend Integration Test Suite...")
        
        try:
            # Mensaje de limpieza de datos
            test_passed = self.integration_test()
            
            # Mensaje de verificación de limpieza
            print("\n🧹 Cleaning up test data...")
            cleanup_success = self.cleanup_test_data()
            
            # Mensaje de generación de reporte PDF
            print("🔍 Verifying data cleanup...")
            verification_passed = self.verify_cleanup()
            
            self.end_time = datetime.now().strftime("%H:%M:%S")
            
            # Mensaje de generación de reporte PDF
            print("\n📄 Generating PDF report...")
            report_file = self.generate_pdf_report()
            
            # Mensaje de los resultados del test
            print(f"\n📊 Test Suite Complete!")
            print(f"Integration Test: {'PASSED' if test_passed else 'FAILED'}")
            print(f"Data Cleanup: {'PASSED' if cleanup_success else 'FAILED'}")
            print(f"Cleanup Verification: {'PASSED' if verification_passed else 'FAILED'}")
            print(f"PDF Report: {report_file}")
            
            return test_passed and cleanup_success and verification_passed
            
        except Exception as e:
            self.end_time = datetime.now().strftime("%H:%M:%S")
            self.log_result("Test Suite", "FAIL", f"Test suite failed: {str(e)}")
            self.generate_pdf_report()
            return False

if __name__ == "__main__":
    runner = BackEndTestRunner()
    success = runner.run_full_test()
    exit(0 if success else 1)
