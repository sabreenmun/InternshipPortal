from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/employer/', views.register_employer, name='register_employer'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/faculty/', views.register_faculty, name='register_faculty'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/resetpass/', views.reset_password, name='reset_password'),
]