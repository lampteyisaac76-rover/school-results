from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/logout/', views.teacher_logout, name='teacher_logout'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
]
