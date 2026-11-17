from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Student


class StudentModelAndViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher_password = "teacherSecretPassword123"
        self.teacher = User.objects.create_user(
            username='teacher',
            password=self.teacher_password,
            is_staff=False
        )

        self.student1 = Student.objects.create(
            admission_number="ADM001",
            first_name="Isaac",
            last_name="Mensah",
            class_name="Basic 7"
        )
        self.student2 = Student.objects.create(
            admission_number="ADM002",
            first_name="Isaac",
            last_name="Owusu",
            class_name="Basic 8"
        )
        self.student3 = Student.objects.create(
            admission_number="ADM003",
            first_name="Kwame",
            last_name="Appiah",
            class_name="Basic 7"
        )

    def test_student_properties(self):
        self.assertEqual(self.student1.full_name, "Isaac Mensah")
        self.assertEqual(self.student1.index_number, "ADM001")
        self.assertIn("Isaac Mensah (ADM001)", str(self.student1))

    def test_unique_admission_number(self):
        with self.assertRaises(IntegrityError):
            Student.objects.create(
                admission_number="ADM001",  # duplicate
                first_name="Another",
                last_name="Student",
                class_name="Basic 7"
            )

    def test_teacher_students_list_requires_login(self):
        response = self.client.get(reverse('teacher_students'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('teacher_login'), response.url)

    def test_teacher_students_list_authenticated(self):
        self.client.login(username='teacher', password=self.teacher_password)
        response = self.client.get(reverse('teacher_students'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Isaac Mensah")
        self.assertContains(response, "ADM001")
        self.assertContains(response, "ADM002")
        self.assertContains(response, "ADM003")

    def test_teacher_student_search_by_name(self):
        self.client.login(username='teacher', password=self.teacher_password)
        response = self.client.get(reverse('teacher_students'), {'q': 'Kwame'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kwame Appiah")
        self.assertNotContains(response, "Isaac Mensah")

    def test_teacher_student_search_by_admission_number(self):
        self.client.login(username='teacher', password=self.teacher_password)
        response = self.client.get(reverse('teacher_students'), {'q': 'ADM002'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Isaac Owusu")
        self.assertNotContains(response, "Kwame Appiah")
