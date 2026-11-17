from django.db import models


class Student(models.Model):
    admission_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Admission Number"
    )
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    class_name = models.CharField(max_length=20, verbose_name="Class")
    date_registered = models.DateTimeField(auto_now_add=True, verbose_name="Date Registered")

    class Meta:
        ordering = ['class_name', 'last_name', 'first_name']
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.admission_number})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def index_number(self):
        """Backwards compatibility alias for admission_number."""
        return self.admission_number

    @index_number.setter
    def index_number(self, value):
        self.admission_number = value
