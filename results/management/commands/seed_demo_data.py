from django.core.management.base import BaseCommand
from students.models import Student
from results.models import Subject, Result


DEMO_STUDENTS = [
    {
        "admission_number": "SCH/2026/001",
        "first_name": "Isaac",
        "last_name": "Mensah",
        "class_name": "Basic 7A",
        # Complete results
        "scores": [85, 92, 78, 88, 90, 84, 86, 79, 82],
    },
    {
        "admission_number": "SCH/2026/002",
        "first_name": "Isaac",
        "last_name": "Owusu",
        "class_name": "Basic 7B",
        # Partial / Incomplete results (only 5 subjects)
        "scores": [74, 80, 68, 72, 75, None, None, None, None],
    },
    {
        "admission_number": "SCH/2026/003",
        "first_name": "Akosua",
        "last_name": "Boateng",
        "class_name": "Basic 7A",
        # Complete results
        "scores": [95, 90, 94, 91, 96, 89, 92, 88, 93],
    },
    {
        "admission_number": "SCH/2026/004",
        "first_name": "Kofi",
        "last_name": "Asante",
        "class_name": "Basic 7B",
        # Not started (0 subjects)
        "scores": [None] * 9,
    },
    {
        "admission_number": "SCH/2026/005",
        "first_name": "Ama",
        "last_name": "Serwaa",
        "class_name": "Basic 8",
        # Complete results
        "scores": [65, 70, 62, 58, 64, 66, 68, 60, 63],
    },
]


class Command(BaseCommand):
    help = "Seed realistic demo student records and examination results for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing demo students and results first',
        )

    def handle(self, *args, **options):
        if options['clear']:
            Result.objects.all().delete()
            Student.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared existing students and results."))

        subjects = list(Subject.objects.all().order_by('name'))
        if len(subjects) < 9:
            self.stderr.write("Subjects not yet populated. Please run: python manage.py populate_subjects first.")
            return

        created_students = 0
        created_results = 0

        for item in DEMO_STUDENTS:
            student, created = Student.objects.get_or_create(
                admission_number=item["admission_number"],
                defaults={
                    "first_name": item["first_name"],
                    "last_name": item["last_name"],
                    "class_name": item["class_name"],
                }
            )
            if created:
                created_students += 1

            for subj, score in zip(subjects, item["scores"]):
                if score is not None:
                    _, res_created = Result.objects.update_or_create(
                        student=student,
                        subject=subj,
                        defaults={"score": score}
                    )
                    if res_created:
                        created_results += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded demo data: {created_students} students, {created_results} results."
        ))
