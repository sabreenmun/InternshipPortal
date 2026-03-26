from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/company-profile/', views.create_company_profile, name='company_profile'),
    path('employer/create-internship/', views.create_internship, name='create_internship'),
    path('employer/internship/<str:internship_id>/applications/', views.application_list, name='application_list'),
    path('employer/application/<int:application_id>/select/', views.select_student, name='select_student'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/profile/', views.create_student_profile, name='student_profile'),
    path('student/search-internships/', views.search_internships, name='search_internships'),
    path('student/internship/<str:internship_id>/', views.internship_detail, name='internship_detail'),
    path('student/application/<int:application_id>/co-op-opt-in/', views.co_op_opt_in, name='co_op_opt_in'),
    path('student/application/<int:application_id>/co-op-summary/', views.submit_coop_summary, name='submit_coop_summary'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty/profile/', views.create_faculty_profile, name='faculty_profile'),
    path('faculty/application/<int:application_id>/grade/', views.grade_student, name='grade_student'),
    path('employer/internship/<str:internship_id>/edit/',
     views.edit_internship, name='edit_internship'),


]