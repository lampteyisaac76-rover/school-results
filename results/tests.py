from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from students.models import Student
from .models import Subject, Result
from .utils import get_student_results_summary, get_overall_performance, GRADING_SCALE


class ResultsAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher_password = "teacherSecretPassword123"
        self.teacher = User.objects.create_user(
            username='teacher',
            password=self.teacher_password,
            is_staff=False
        )

        # Create the standard 9 subjects
        self.subject_names = [
            "Mathematics",
            "English Language",
            "Integrated Science",
            "Social Studies",
            "Computing",
            "RME",
            "Ghanaian Language",
            "Creative Arts",
            "Career Technology",
        ]
        self.subjects = [Subject.objects.create(name=n) for n in self.subject_names]

        # Create test students
        self.student1 = Student.objects.create(
            admission_number="STU-001",
            first_name="Isaac",
            last_name="Mensah",
            class_name="JHS 1"
        )
        self.student2 = Student.objects.create(
            admission_number="STU-002",
            first_name="isaac",
            last_name="Owusu",
            class_name="JHS 2"
        )
        self.student3 = Student.objects.create(
            admission_number="STU-003",
            first_name="Akosua",
            last_name="Boateng",
            class_name="JHS 1"
        )

    def test_score_database_constraint(self):
        # Result score should be between 0 and 100
        valid_result = Result.objects.create(
            student=self.student1,
            subject=self.subjects[0],
            score=85
        )
        self.assertEqual(valid_result.score, 85)

        # Unique together constraint
        with self.assertRaises(IntegrityError):
            Result.objects.create(
                student=self.student1,
                subject=self.subjects[0],
                score=90
            )

    def test_teacher_score_entry_success(self):
        self.client.login(username='teacher', password=self.teacher_password)
        post_data = {}
        # Give scores: 80, 85, 90, 75, 70, 80, 85, 90, 95
        sample_scores = [80, 85, 90, 75, 70, 80, 85, 90, 95]
        for subj, sc in zip(self.subjects, sample_scores):
            post_data[f"score_{subj.id}"] = str(sc)

        response = self.client.post(
            reverse('teacher_enter_scores', args=[self.student1.id]),
            data=post_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('teacher_students'))

        # Verify all 9 scores are saved
        results = Result.objects.filter(student=self.student1)
        self.assertEqual(results.count(), 9)

        # Check total and average
        summary = get_student_results_summary(self.student1)
        self.assertTrue(summary['is_complete'])
        expected_total = sum(sample_scores)
        expected_avg = round(expected_total / 9.0, 2)
        self.assertEqual(summary['total_score'], expected_total)
        self.assertEqual(summary['average_score'], expected_avg)
        self.assertIsNotNone(summary['overall_performance'])

    def test_teacher_score_entry_update_no_duplicate(self):
        # First save an initial score
        Result.objects.create(
            student=self.student1,
            subject=self.subjects[0],
            score=50
        )

        self.client.login(username='teacher', password=self.teacher_password)
        post_data = {f"score_{self.subjects[0].id}": "88"}

        response = self.client.post(
            reverse('teacher_enter_scores', args=[self.student1.id]),
            data=post_data
        )
        self.assertEqual(response.status_code, 302)

        # Still only 1 result for this subject, score updated to 88
        results = Result.objects.filter(student=self.student1, subject=self.subjects[0])
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().score, 88)

    def test_teacher_score_entry_validation_errors(self):
        self.client.login(username='teacher', password=self.teacher_password)

        # Test score > 100
        post_data = {f"score_{self.subjects[0].id}": "150"}
        response = self.client.post(
            reverse('teacher_enter_scores', args=[self.student1.id]),
            data=post_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "must be between 0 and 100")

        # Test negative score
        post_data = {f"score_{self.subjects[0].id}": "-5"}
        response = self.client.post(
            reverse('teacher_enter_scores', args=[self.student1.id]),
            data=post_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "must be between 0 and 100")

        # Test non-integer score
        post_data = {f"score_{self.subjects[0].id}": "eighty"}
        response = self.client.post(
            reverse('teacher_enter_scores', args=[self.student1.id]),
            data=post_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "must be a whole number")

    def test_parent_search_case_insensitive(self):
        # Searching "isaac", "Isaac", "ISAAC" should return both Isaac Mensah and isaac Owusu
        for search_term in ["isaac", "Isaac", "ISAAC"]:
            response = self.client.get(reverse('parent_search'), {'first_name': search_term})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Isaac Mensah")
            self.assertContains(response, "isaac Owusu")
            self.assertNotContains(response, "Akosua Boateng")

    def test_parent_search_not_found(self):
        response = self.client.get(reverse('parent_search'), {'first_name': 'UnknownName'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Student Found")
        self.assertContains(response, "UnknownName")

    def test_incomplete_results_display(self):
        # Enter only 3 of 9 subjects
        for i in range(3):
            Result.objects.create(
                student=self.student3,
                subject=self.subjects[i],
                score=75
            )

        summary = get_student_results_summary(self.student3)
        self.assertFalse(summary['is_complete'])
        self.assertIsNone(summary['total_score'])
        self.assertIsNone(summary['average_score'])
        self.assertIsNone(summary['overall_performance'])

        response = self.client.get(reverse('student_results', args=[self.student3.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Incomplete Examination Results")
        self.assertContains(response, "Scores have only been recorded for")
        self.assertContains(response, "3")
        # Should not display calculated misleading totals
        self.assertNotContains(response, "9 Subjects Sum")

    def test_complete_results_display(self):
        # Enter all 9 subjects with score 80
        for subj in self.subjects:
            Result.objects.create(
                student=self.student3,
                subject=subj,
                score=80
            )

        summary = get_student_results_summary(self.student3)
        self.assertTrue(summary['is_complete'])
        self.assertEqual(summary['total_score'], 720)
        self.assertEqual(summary['average_score'], 80.0)
        self.assertEqual(summary['overall_performance']['grade'], "Grade 1")

        response = self.client.get(reverse('student_results', args=[self.student3.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "720")
        self.assertContains(response, "80.0%")
        self.assertContains(response, "Grade 1")
        self.assertNotContains(response, "Incomplete Examination Results")
