from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'first_name', 'last_name', 'class_name', 'date_registered')
    search_fields = ('admission_number', 'first_name', 'last_name', 'class_name')
    list_filter = ('class_name', 'date_registered')
    ordering = ('class_name', 'last_name', 'first_name')
