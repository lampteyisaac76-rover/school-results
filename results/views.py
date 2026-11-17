from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction, models
from django.db.models import Q
from students.models import Student
from .models import Subject, Result
from .utils import get_student_results_summary


@login_required(login_url='teacher_login')
def teacher_enter_scores(request, student_id):
    """
    Teacher portal view to enter and update scores for all subjects for a student.
    Validates that all entered scores are whole numbers between 0 and 100.
    Prevents duplicates by updating existing results.
    """
    student = get_object_or_404(Student, id=student_id)
    subjects = Subject.objects.all().order_by('name')

    # Load existing results for this student
    existing_results = {r.subject_id: r.score for r in Result.objects.filter(student=student)}

    errors = {}
    form_scores = {}

    if request.method == 'POST':
        cleaned_scores = {}

        for subj in subjects:
            field_name = f"score_{subj.id}"
            raw_val = request.POST.get(field_name, '').strip()
            form_scores[subj.id] = raw_val

            if raw_val == '':
                cleaned_scores[subj.id] = None
                continue

            # Validate whole number
            try:
                # Must be an integer (e.g., '85', not '85.5' or 'abc')
                score_int = int(raw_val)
            except ValueError:
                errors[subj.id] = f"Score for {subj.name} must be a whole number between 0 and 100."
                continue

            # Validate range 0 - 100
            if score_int < 0 or score_int > 100:
                errors[subj.id] = f"Score for {subj.name} must be between 0 and 100 (got {score_int})."
                continue

            cleaned_scores[subj.id] = score_int

        if not errors:
            with transaction.atomic():
                for subj in subjects:
                    val = cleaned_scores.get(subj.id)
                    if val is not None:
                        Result.objects.update_or_create(
                            student=student,
                            subject=subj,
                            defaults={'score': val}
                        )
                    else:
                        # If a teacher explicitly left it empty, remove any previous entry if existed
                        Result.objects.filter(student=student, subject=subj).delete()

            messages.success(
                request,
                f"Examination scores for {student.full_name} ({student.admission_number}) have been successfully saved."
            )
            return redirect('teacher_students')
        else:
            messages.error(request, "Please correct the errors indicated below before saving.")
    else:
        # Initial GET: populate from existing database results
        for subj in subjects:
            if subj.id in existing_results:
                form_scores[subj.id] = existing_results[subj.id]
            else:
                form_scores[subj.id] = ''

    # Build rows for the template
    subject_rows = []
    for subj in subjects:
        subject_rows.append({
            'subject': subj,
            'current_value': form_scores.get(subj.id, ''),
            'error': errors.get(subj.id),
        })

    return render(request, 'results/teacher_enter_scores.html', {
        'student': student,
        'subject_rows': subject_rows,
        'total_subjects': subjects.count(),
    })


def parent_search(request):
    """
    Public results search page for parents.
    Allows parents to search by student's first name (case-insensitive).
    Displays matching students with full name, admission number, and class.
    """
    first_name_query = request.GET.get('first_name', '').strip()
    searched = bool(first_name_query)
    matched_students = []

    if searched:
        matched_students = Student.objects.filter(
            Q(first_name__iexact=first_name_query) |
            Q(last_name__iexact=first_name_query) |
            Q(first_name__icontains=first_name_query) |
            Q(last_name__icontains=first_name_query) |
            Q(admission_number__iexact=first_name_query)
        ).distinct().order_by('class_name', 'last_name', 'first_name')

    return render(request, 'results/parent_search.html', {
        'searched': searched,
        'first_name_query': first_name_query,
        'matched_students': matched_students,
    })


def student_results(request, student_id):
    """
    Public student results display page.
    Renders official results slip with all subjects, total score, average,
    and overall performance. Clearly flags incomplete results without misleading totals.
    """
    student = get_object_or_404(Student, id=student_id)
    summary = get_student_results_summary(student)

    return render(request, 'results/student_results.html', {
        'summary': summary,
    })
