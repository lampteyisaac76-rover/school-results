from django.urls import path
from . import views

urlpatterns = [
    path('results/', views.parent_search, name='parent_search'),
    path('results/student/<int:student_id>/', views.student_results, name='student_results'),
    path('teacher/students/<int:student_id>/scores/', views.teacher_enter_scores, name='teacher_enter_scores'),
]
