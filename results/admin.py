from django.contrib import admin
from .models import Subject, Result


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score', 'date_entered')
    search_fields = (
        'student__admission_number',
        'student__first_name',
        'student__last_name',
        'subject__name',
    )
    list_filter = ('subject', 'student__class_name', 'date_entered')
    ordering = ('student__class_name', 'student__last_name', 'subject__name')
