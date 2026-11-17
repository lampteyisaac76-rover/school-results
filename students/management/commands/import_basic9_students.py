from django.core.management.base import BaseCommand
from students.models import Student


BASIC_9_STUDENTS = [
    {
        "sn": 1,
        "admission_number": "0115182001",
        "first_name": "Asana",
        "last_name": "Abdul Rahman",
        "class_name": "Basic 9",
    },
    {
        "sn": 2,
        "admission_number": "0115182002",
        "first_name": "Kirby Kwesi Acheampong",
        "last_name": "Adams",
        "class_name": "Basic 9",
    },
    {
        "sn": 3,
        "admission_number": "0115182003",
        "first_name": "Caleb",
        "last_name": "Aidoo",
        "class_name": "Basic 9",
    },
    {
        "sn": 4,
        "admission_number": "0115182004",
        "first_name": "Desmond",
        "last_name": "Amponsah",
        "class_name": "Basic 9",
    },
    {
        "sn": 5,
        "admission_number": "0115182005",
        "first_name": "Nhyiraba Gyamfi Boateng",
        "last_name": "Appiah",
        "class_name": "Basic 9",
    },
    {
        "sn": 6,
        "admission_number": "0115182006",
        "first_name": "Sahadatu S.",
        "last_name": "Atitsu",
        "class_name": "Basic 9",
    },
    {
        "sn": 7,
        "admission_number": "0115182007",
        "first_name": "Ruben Adjei",
        "last_name": "Boadi",
        "class_name": "Basic 9",
    },
    {
        "sn": 8,
        "admission_number": "0115182008",
        "first_name": "Erica Akosua Obeyaa",
        "last_name": "Bosompem",
        "class_name": "Basic 9",
    },
    {
        "sn": 9,
        "admission_number": "0115182009",
        "first_name": "Lydia Aseda",
        "last_name": "Bredu",
        "class_name": "Basic 9",
    },
    {
        "sn": 10,
        "admission_number": "01151820010",
        "first_name": "Bright",
        "last_name": "Ewusi",
        "class_name": "Basic 9",
    },
    {
        "sn": 11,
        "admission_number": "01151820011",
        "first_name": "Joseph Mintah",
        "last_name": "Fobi",
        "class_name": "Basic 9",
    },
    {
        "sn": 12,
        "admission_number": "01151820012",
        "first_name": "Ernest Fiifi",
        "last_name": "Greenslade",
        "class_name": "Basic 9",
    },
    {
        "sn": 13,
        "admission_number": "01151820013",
        "first_name": "Bettina Nana Abena",
        "last_name": "Ofosu",
        "class_name": "Basic 9",
    },
    {
        "sn": 14,
        "admission_number": "01151820014",
        "first_name": "Lawrencia Ama",
        "last_name": "Oparebea",
        "class_name": "Basic 9",
    },
    {
        "sn": 15,
        "admission_number": "01151820015",
        "first_name": "Edna Kwatema",
        "last_name": "Owusu",
        "class_name": "Basic 9",
    },
    {
        "sn": 16,
        "admission_number": "01151820016",
        "first_name": "Emmanuel Larbi Jr.",
        "last_name": "Quaye",
        "class_name": "Basic 9",
    },
    {
        "sn": 17,
        "admission_number": "01151820017",
        "first_name": "Bertha",
        "last_name": "Sarfo",
        "class_name": "Basic 9",
    },
    {
        "sn": 18,
        "admission_number": "01151820018",
        "first_name": "Abraham",
        "last_name": "Setie",
        "class_name": "Basic 9",
    },
]


class Command(BaseCommand):
    help = "Import the 18 Basic 9 students in the exact specified order with admission numbers starting with 011518200"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing students first before importing',
        )

    def handle(self, *args, **options):
        if options['clear']:
            deleted_count, _ = Student.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Cleared {deleted_count} existing student records."))

        created_count = 0
        updated_count = 0

        for item in BASIC_9_STUDENTS:
            student, created = Student.objects.update_or_create(
                admission_number=item["admission_number"],
                defaults={
                    "first_name": item["first_name"],
                    "last_name": item["last_name"],
                    "class_name": item["class_name"],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f"[{item['sn']:02d}] Created: {student.full_name} ({student.admission_number}) - {student.class_name}"
                ))
            else:
                updated_count += 1
                self.stdout.write(
                    f"[{item['sn']:02d}] Updated: {student.full_name} ({student.admission_number}) - {student.class_name}"
                )

        self.stdout.write(self.style.SUCCESS(
            f"\nFinished! Created: {created_count}, Updated: {updated_count}. Total Basic 9 students: {Student.objects.filter(class_name='Basic 9').count()}"
        ))
