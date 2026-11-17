from django.core.management.base import BaseCommand
from results.models import Subject


DEFAULT_SUBJECTS = [
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


class Command(BaseCommand):
    help = "Populate the standard 9 school subjects"

    def handle(self, *args, **options):
        created_count = 0
        for name in DEFAULT_SUBJECTS:
            subject, created = Subject.objects.get_or_create(name=name)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created subject: {name}"))
            else:
                self.stdout.write(f"Subject already exists: {name}")

        self.stdout.write(self.style.SUCCESS(
            f"Done! {created_count} new subjects created. Total subjects: {Subject.objects.count()}"
        ))
