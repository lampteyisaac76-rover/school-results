from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from .models import Student
from results.models import Subject


@login_required(login_url='teacher_login')
def teacher_students(request):
    """
    Teacher student list and search page.
    Allows teachers to browse registered students, search by name or admission number,
    view scoring progress, and select a student to enter/update examination scores.
    """
    query = request.GET.get('q', '').strip()
    selected_class = request.GET.get('class', '').strip()

    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(admission_number__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    if selected_class:
        students = students.filter(class_name=selected_class)

    total_subjects = Subject.objects.count()

    students = students.annotate(results_count=Count('results')).order_by('class_name', 'last_name', 'first_name')

    available_classes = Student.objects.values_list('class_name', flat=True).distinct().order_by('class_name')

    return render(request, 'students/teacher_students.html', {
        'students': students,
        'query': query,
        'selected_class': selected_class,
        'available_classes': available_classes,
        'total_subjects': total_subjects,
    })
