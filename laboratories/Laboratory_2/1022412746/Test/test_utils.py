import requests
import json
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

class TestDataTracker:
    """Tracks test data to ensure proper cleanup"""
    
    def __init__(self):
        self.created_users = []
        self.created_tasks = []
        self.test_results = []
        
    def track_user(self, user_id):
        """Track a user created during testing"""
        self.created_users.append(user_id)
        
    def track_task(self, task_id):
        """Track a task created during testing"""
        self.created_tasks.append(task_id)
        
    def add_test_result(self, test_name, status, details=""):
        """Add a test result for reporting"""
        self.test_results.append({
            'test_name': test_name,
            'status': status,
            'details': details,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    def cleanup_all_data(self):
        """Clean up all tracked test data"""
        cleanup_results = {
            'users_deleted': 0,
            'tasks_deleted': 0,
            'errors': []
        }
        
        # Clean up tasks first (due to foreign key constraints)
        if self.created_tasks:
            try:
                # Use specific cleanup endpoint for better control
                response = requests.delete(
                    'http://localhost:5002/tasks/cleanup-specific',
                    json={'task_ids': self.created_tasks}
                )
                if response.status_code == 200:
                    cleanup_results['tasks_deleted'] = len(self.created_tasks)
                else:
                    cleanup_results['errors'].append(f"Failed to delete tasks: {response.text}")
            except Exception as e:
                cleanup_results['errors'].append(f"Error deleting tasks: {str(e)}")
        
        # Clean up users
        if self.created_users:
            try:
                # Use specific cleanup endpoint for better control  
                response = requests.delete(
                    'http://localhost:5001/users/cleanup-specific',
                    json={'user_ids': self.created_users}
                )
                if response.status_code == 200:
                    cleanup_results['users_deleted'] = len(self.created_users)
                else:
                    cleanup_results['errors'].append(f"Failed to delete users: {response.text}")
            except Exception as e:
                cleanup_results['errors'].append(f"Error deleting users: {str(e)}")
        
        # Clear tracking lists
        self.created_users.clear()
        self.created_tasks.clear()
        
        return cleanup_results
        
    def verify_cleanup(self):
        """Verify that all tracked data has been deleted"""
        verification_results = {
            'users_still_exist': [],
            'tasks_still_exist': [],
            'cleanup_verified': True
        }
        
        # Check if users still exist
        for user_id in self.created_users:
            try:
                response = requests.get(f'http://localhost:5001/users/{user_id}')
                if response.status_code == 200:
                    verification_results['users_still_exist'].append(user_id)
                    verification_results['cleanup_verified'] = False
            except Exception as e:
                # If we get an error, assume the user doesn't exist
                pass
        
        # Check if tasks still exist
        try:
            response = requests.get('http://localhost:5002/tasks')
            if response.status_code == 200:
                all_tasks = response.json()
                for task_id in self.created_tasks:
                    if any(t['id'] == task_id for t in all_tasks):
                        verification_results['tasks_still_exist'].append(task_id)
                        verification_results['cleanup_verified'] = False
        except Exception as e:
            verification_results['cleanup_verified'] = False
        
        return verification_results

class PDFReportGenerator:
    """Generates PDF reports for test results"""
    
    def __init__(self, report_dir="test_reports"):
        self.report_dir = report_dir
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
    
    def get_next_report_number(self):
        """Get the next sequential report number"""
        existing_files = [f for f in os.listdir(self.report_dir) if f.startswith('test_report_') and f.endswith('.pdf')]
        if not existing_files:
            return 1
        
        numbers = []
        for file in existing_files:
            try:
                # Extract number from filename like 'test_report_001.pdf'
                number_str = file.replace('test_report_', '').replace('.pdf', '')
                numbers.append(int(number_str))
            except ValueError:
                continue
        
        return max(numbers) + 1 if numbers else 1
    
    def generate_report(self, test_results, cleanup_results, verification_results, test_type="Backend"):
        """Generate a comprehensive PDF report"""
        report_number = self.get_next_report_number()
        filename = f"test_report_{report_number:03d}.pdf"
        filepath = os.path.join(self.report_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter, topMargin=0.5*inch)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=20,
            textColor=colors.darkblue,
            spaceAfter=30
        )
        story.append(Paragraph(f"Integration Test Report #{report_number:03d}", title_style))
        story.append(Spacer(1, 12))
        
        # Test Information
        info_style = ParagraphStyle(
            'Info',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12
        )
        story.append(Paragraph(f"<b>Test Type:</b> {test_type}", info_style))
        story.append(Paragraph(f"<b>Execution Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", info_style))
        story.append(Paragraph(f"<b>Total Tests:</b> {len(test_results)}", info_style))
        story.append(Spacer(1, 20))
        
        # Test Results Summary
        passed_tests = sum(1 for result in test_results if result['status'] == 'PASSED')
        failed_tests = len(test_results) - passed_tests
        
        summary_data = [
            ['Test Status', 'Count', 'Percentage'],
            ['PASSED', str(passed_tests), f"{(passed_tests/len(test_results)*100):.1f}%" if test_results else "0%"],
            ['FAILED', str(failed_tests), f"{(failed_tests/len(test_results)*100):.1f}%" if test_results else "0%"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 1*inch, 1*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Detailed Test Results
        story.append(Paragraph("<b>Detailed Test Results</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        if test_results:
            test_data = [['Test Name', 'Status', 'Timestamp', 'Details']]
            for result in test_results:
                test_data.append([
                    result['test_name'],
                    result['status'],  # Simplified - just the status text without HTML
                    result['timestamp'],
                    result['details'][:50] + "..." if len(result['details']) > 50 else result['details']
                ])
            
            test_table = Table(test_data, colWidths=[2*inch, 1*inch, 1.5*inch, 2*inch])
            test_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                # Add conditional text color for status column based on content
                ('TEXTCOLOR', (1, 1), (1, -1), colors.green),  # Default to green for status column
            ]))
            
            # Apply red color to FAILED status entries
            for i, result in enumerate(test_results):
                if result['status'] == 'FAILED':
                    test_table.setStyle(TableStyle([
                        ('TEXTCOLOR', (1, i+1), (1, i+1), colors.red)
                    ]))
                    
            story.append(test_table)
        else:
            story.append(Paragraph("No test results to display", styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Cleanup Results
        story.append(Paragraph("<b>Data Cleanup Results</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        cleanup_data = [
            ['Cleanup Action', 'Result'],
            ['Users Deleted', str(cleanup_results.get('users_deleted', 0))],
            ['Tasks Deleted', str(cleanup_results.get('tasks_deleted', 0))],
            ['Errors', str(len(cleanup_results.get('errors', [])))]
        ]
        
        cleanup_table = Table(cleanup_data, colWidths=[3*inch, 2*inch])
        cleanup_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(cleanup_table)
        
        # Cleanup Verification
        story.append(Spacer(1, 20))
        story.append(Paragraph("<b>Cleanup Verification</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        verification_status = "VERIFIED" if verification_results['cleanup_verified'] else "FAILED"
        
        # Create a simple table for verification status without HTML tags
        verification_data = [
            ['Cleanup Status', verification_status]
        ]
        
        verification_table = Table(verification_data, colWidths=[3*inch, 2*inch])
        verification_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('TEXTCOLOR', (1, 0), (1, 0), colors.green if verification_results['cleanup_verified'] else colors.red),
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold')
        ]))
        story.append(verification_table)
        
        if not verification_results['cleanup_verified']:
            if verification_results['users_still_exist']:
                story.append(Paragraph(f"Users still exist: {verification_results['users_still_exist']}", styles['Normal']))
            if verification_results['tasks_still_exist']:
                story.append(Paragraph(f"Tasks still exist: {verification_results['tasks_still_exist']}", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        print(f"[SUCCESS] PDF report generated: {filepath}")
        return filepath
