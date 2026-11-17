from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from students.models import Student


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Subject Name")

    class Meta:
        ordering = ['name']
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name


class Result(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name="Student"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name="Subject"
    )
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Score"
    )
    date_entered = models.DateTimeField(auto_now=True, verbose_name="Date Entered")

    class Meta:
        unique_together = ('student', 'subject')
        constraints = [
            models.CheckConstraint(
                condition=models.Q(score__gte=0) & models.Q(score__lte=100),
                name='score_range_0_100'
            )
        ]
        ordering = ['subject__name']
        verbose_name = "Result"
        verbose_name_plural = "Results"

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.name}: {self.score}"
