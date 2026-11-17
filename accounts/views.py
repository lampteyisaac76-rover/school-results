from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from students.models import Student
from results.models import Subject, Result


def home(request):
    """Public landing page for the School Results Portal."""
    total_subjects = Subject.objects.count()
    return render(request, 'home.html', {
        'total_subjects': total_subjects,
    })


def teacher_login(request):
    """
    Teacher login view using the shared teacher account credentials.
    Asks for the teacher password and authenticates against the 'teacher' user.
    """
    if request.user.is_authenticated:
        return redirect('teacher_dashboard')

    error = ""
    if request.method == 'POST':
        password = request.POST.get('password', '').strip()

        user = authenticate(
            request,
            username='teacher',
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, "Welcome to the Teacher Portal!")
            return redirect('teacher_dashboard')
        else:
            error = "Incorrect password. Please try again."

    return render(request, 'accounts/teacher_login.html', {'error': error})


def teacher_logout(request):
    """Logs out the teacher session and redirects to login."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('teacher_login')


@login_required(login_url='teacher_login')
def teacher_dashboard(request):
    """
    Teacher dashboard providing access to registered students,
    quick search, results completion status, and score entry links.
    """
    total_students = Student.objects.count()
    total_subjects = Subject.objects.count()

    # Calculate completion metrics
    students_with_results = Student.objects.annotate(
        results_count=Count('results')
    )
    
    complete_count = 0
    partial_count = 0
    not_started_count = 0

    for s in students_with_results:
        if total_subjects > 0 and s.results_count >= total_subjects:
            complete_count += 1
        elif s.results_count > 0:
            partial_count += 1
        else:
            not_started_count += 1

    # Quick search if submitted from dashboard
    query = request.GET.get('q', '').strip()
    search_results = None
    if query:
        search_results = Student.objects.filter(
            Q(admission_number__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(class_name__icontains=query)
        ).annotate(results_count=Count('results'))

    # Recent students for quick access
    recent_students = Student.objects.all().order_by('-id')[:6].annotate(
        results_count=Count('results')
    )

    return render(request, 'accounts/teacher_dashboard.html', {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'complete_count': complete_count,
        'partial_count': partial_count,
        'not_started_count': not_started_count,
        'search_query': query,
        'search_results': search_results,
        'recent_students': recent_students,
    })
