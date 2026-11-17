from django.urls import path
from . import views

urlpatterns = [
    path('teacher/students/', views.teacher_students, name='teacher_students'),
]
