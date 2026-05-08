from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Task, UserProfile

class TaskAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123'
        )

        UserProfile.objects.create(
            user=self.admin_user,
            role='ADMIN'
        )

        self.employee = User.objects.create_user(
            username='employee',
            password='employee123'
        )

        UserProfile.objects.create(
            user=self.employee,
            role='EMPLOYEE'
        )

        self.client.force_authenticate(user=self.admin_user)

    def test_create_task(self):
        response = self.client.post('/api/tasks/', {
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'PENDING',
            'assigned_to_id': self.employee.id
        })

        self.assertEqual(response.status_code, 201)

    def test_get_tasks(self):
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        task = Task.objects.create(
            title='Old',
            description='Old Desc',
            created_by=self.admin_user,
            assigned_to=self.employee
        )

        response = self.client.put(f'/api/tasks/{task.id}/', {
            'title': 'Updated',
            'description': 'Updated Desc',
            'status': 'COMPLETED',
            'assigned_to_id': self.employee.id
        })

        self.assertEqual(response.status_code, 200)

    def test_delete_task(self):
        task = Task.objects.create(
            title='Delete',
            description='Delete Desc',
            created_by=self.admin_user,
            assigned_to=self.employee
        )

        response = self.client.delete(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, 204)

    def test_employee_cannot_create_task(self):
        self.client.force_authenticate(user=self.employee)

        response = self.client.post('/api/tasks/', {
            'title': 'Not Allowed',
            'description': 'Denied',
            'status': 'PENDING',
            'assigned_to_id': self.employee.id
        })

        self.assertEqual(response.status_code, 403)
