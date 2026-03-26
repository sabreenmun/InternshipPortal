from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from portal.models import Company, Student, Faculty
from django.urls import reverse


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def register_employer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            return render(request, 'accounts/register_employer.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register_employer.html', {'error': 'Username already exists'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register_employer.html', {'error': 'Email already exists'})
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        
        # create company profile
        company = Company(
            employer=user,
            name=request.POST.get('name'),
            location=request.POST.get('location'),
            website=request.POST.get('website'),
            contact_person_name=request.POST.get('contact_person_name'),
            contact_person_email=request.POST.get('contact_person_email'),
            contact_person_phone=request.POST.get('contact_person_phone')
        )
        
        # generate unique employer ID
        last_employer = Company.objects.order_by('id').last()
        new_id = last_employer.id + 1 if last_employer else 1
        company.employer_unique_id = f"EMP{new_id:04d}"
        
        company.save()
        
        #set user type
        user.userprofile.user_type = 'employer'
        user.userprofile.save()
        
        login(request, user)
        return redirect('employer_dashboard')
    
    return render(request, 'accounts/register_employer.html')

def register_student(request):
    if request.method == 'POST':
        #create user account
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            return render(request, 'accounts/register_student.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register_student.html', {'error': 'Username already exists'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register_student.html', {'error': 'Email already exists'})
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        
        #create student profile
        student = Student(
            user=user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone_number=request.POST.get('phone_number'),
            department=request.POST.get('department'),
            major=request.POST.get('major'),
            credit_hours=request.POST.get('credit_hours'),
            gpa=request.POST.get('gpa'),
            start_semester=request.POST.get('start_semester'),
            is_transfer=request.POST.get('is_transfer') == 'on'
        )
        
        # hhandle resume upload
        if 'resume' in request.FILES:
            student.resume = request.FILES['resume']
        
        #generate unique student ID
        last_student = Student.objects.order_by('id').last()
        new_id = last_student.id + 1 if last_student else 1
        student.student_id = f"STU{new_id:04d}"
        
        student.save()
        
        # set user type
        user.userprofile.user_type = 'student'
        user.userprofile.save()
        
        login(request, user)
        return redirect('student_dashboard')
    
    return render(request, 'accounts/register_student.html')

def register_faculty(request):
    if request.method == 'POST':
        #create user account
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            return render(request, 'accounts/register_faculty.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register_faculty.html', {'error': 'Username already exists'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/register_faculty.html', {'error': 'Email already exists'})
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        
        #create faculty profile
        faculty = Faculty(
            user=user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('faculty_email'),
            department=request.POST.get('department')
        )
        
        faculty.save()
        
        #set the et user type
        user.userprofile.user_type = 'faculty'
        user.userprofile.save()
        
        login(request, user)
        return redirect('faculty_dashboard')
    
    return render(request, 'accounts/register_faculty.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def dashboard(request):
    user_profile = request.user.userprofile
    context = {
        'user_type': user_profile.user_type,
        'user': request.user
    }
    return render(request, 'accounts/dashboard.html', context)



@login_required
def logout_view(request):
    logout(request)
    return redirect('login') 

def reset_password(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username:
            error = "Please enter your username."
        elif not password1 or not password2:
            error = "Please enter your new password twice."
        elif password1 != password2:
            error = "Passwords do not match."
        else:
            try:
                user = User.objects.get(username=username)
                user.password = make_password(password1)
                user.save()
                # redirect to login page after success
                return redirect(reverse('login'))
            except User.DoesNotExist:
                error = "No user found with that username."

    return render(request, 'accounts/reset_password.html', {'error': error})