from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TeacherAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher_password = "teacherSecretPassword123"
        self.teacher = User.objects.create_user(
            username='teacher',
            password=self.teacher_password,
            is_staff=False,
            is_superuser=False
        )

    def test_unauthenticated_dashboard_redirects_to_login(self):
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('teacher_login'), response.url)

    def test_teacher_login_success(self):
        response = self.client.post(reverse('teacher_login'), {
            'password': self.teacher_password
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('teacher_dashboard'))

        # Check authenticated session
        dashboard_response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertContains(dashboard_response, "Welcome to the Teacher Dashboard")

    def test_teacher_login_wrong_password(self):
        response = self.client.post(reverse('teacher_login'), {
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Incorrect password. Please try again.")

    def test_teacher_logout(self):
        self.client.login(username='teacher', password=self.teacher_password)
        response = self.client.get(reverse('teacher_logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('teacher_login'))

        # Verifying dashboard redirects after logout
        dash_response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(dash_response.status_code, 302)

    def test_teacher_cannot_access_admin(self):
        self.client.login(username='teacher', password=self.teacher_password)
        # Attempt to access django admin
        response = self.client.get('/admin/')
        # Django admin requires is_staff=True. If not staff, it renders login page with error or redirects
        self.assertNotEqual(response.status_code, 200)
        # Even if 302, it redirects to admin login, not the dashboard
        if response.status_code == 302:
            self.assertIn('/admin/login/', response.url)
