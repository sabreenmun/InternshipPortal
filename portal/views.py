from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from .forms import *
from .utils import check_coop_eligibility

def is_employer(user):
    return user.userprofile.user_type == 'employer'

def is_student(user):
    return user.userprofile.user_type == 'student'

def is_faculty(user):
    return user.userprofile.user_type == 'faculty'

@login_required
def home(request):
    user_type = request.user.userprofile.user_type
    if user_type == 'employer':
        return redirect('employer_dashboard')
    elif user_type == 'student':
        return redirect('student_dashboard')
    elif user_type == 'faculty':
        return redirect('faculty_dashboard')
    return redirect('dashboard')

@login_required
@user_passes_test(is_employer)
def employer_dashboard(request):
    company = Company.objects.get(employer=request.user)
    internships = Internship.objects.filter(employer=company)
    context = {
        'company': company,
        'internships': internships,
    }
    return render(request, 'portal/employer_dashboard.html', context)

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    applications = Application.objects.filter(student=student)
    context = {
        'student': student,
        'applications': applications,
    }
    return render(request, 'portal/student_dashboard.html', context)

@login_required
@user_passes_test(is_faculty)
def faculty_dashboard(request):
    faculty = Faculty.objects.get(user=request.user)
    #get co-op students in the same department
    co_op_students = CoopRegistration.objects.filter(
        application__student__department=faculty.department,
        opted_in=True
    )
    context = {
        'faculty': faculty,
        'co_op_students': co_op_students,
    }
    return render(request, 'portal/faculty_dashboard.html', context)

@login_required
@user_passes_test(is_employer)
def create_company_profile(request):
    try:
        company = Company.objects.get(employer=request.user)
        form = CompanyForm(request.POST or None, instance=company)
    except Company.DoesNotExist:
        form = CompanyForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        company = form.save(commit=False)
        company.employer = request.user
        if not company.employer_unique_id:
            # Generate unique employer ID
            last_employer = Company.objects.order_by('id').last()
            new_id = last_employer.id + 1 if last_employer else 1
            company.employer_unique_id = f"EMP{new_id:04d}"
        company.save()
        messages.success(request, 'Company profile saved successfully!')
        return redirect('employer_dashboard')
    
    return render(request, 'portal/company_profile.html', {'form': form})

@login_required
@user_passes_test(is_student)
def create_student_profile(request):
    try:
        student = Student.objects.get(user=request.user)
        form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    except Student.DoesNotExist:
        form = StudentForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST' and form.is_valid():
        student = form.save(commit=False)
        student.user = request.user
        if not student.student_id:
            # Generate unique student ID
            last_student = Student.objects.order_by('id').last()
            new_id = last_student.id + 1 if last_student else 1
            student.student_id = f"STU{new_id:04d}"
        student.save()
        messages.success(request, 'Student profile saved successfully!')
        return redirect('student_dashboard')
    
    return render(request, 'portal/student_profile.html', {'form': form})

@login_required
@user_passes_test(is_faculty)
def create_faculty_profile(request):
    try:
        faculty = Faculty.objects.get(user=request.user)
        form = FacultyForm(request.POST or None, instance=faculty)
    except Faculty.DoesNotExist:
        form = FacultyForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        faculty = form.save(commit=False)
        faculty.user = request.user
        faculty.save()
        messages.success(request, 'Faculty profile saved successfully!')
        return redirect('faculty_dashboard')
    
    return render(request, 'portal/faculty_profile.html', {'form': form})

@login_required
@user_passes_test(is_employer)
def create_internship(request):
    company = Company.objects.get(employer=request.user)
    
    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.employer = company
            
            #generate unique internship ID
            last_internship = Internship.objects.order_by('id').last()
            new_id = last_internship.id + 1 if last_internship else 1
            internship.internship_id = f"INT{new_id:04d}"
            
            internship.save()
            messages.success(request, 'Internship posted successfully!')
            return redirect('employer_dashboard')
    else:
        form = InternshipForm()
    
    return render(request, 'portal/create_internship.html', {'form': form})

@login_required
@user_passes_test(is_student)
def search_internships(request):
    form = InternshipSearchForm(request.GET or None)
    internships = Internship.objects.filter(status='open')
    
    if form.is_valid():
        title = form.cleaned_data.get('title')
        location = form.cleaned_data.get('location')
        major = form.cleaned_data.get('major')
        
        if title:
            internships = internships.filter(title__icontains=title)
        if location:
            internships = internships.filter(location__icontains=location)
        if major:
            internships = internships.filter(majors__icontains=major)
    
    return render(request, 'portal/search_internships.html', {
        'form': form,
        'internships': internships
    })

@login_required
@user_passes_test(is_student)
def internship_detail(request, internship_id):
    internship = get_object_or_404(Internship, internship_id=internship_id)
    student = Student.objects.get(user=request.user)
    
    # check if student has already applied
    has_applied = Application.objects.filter(
        student=student, 
        internship=internship
    ).exists()
    
    if request.method == 'POST' and not has_applied:
        Application.objects.create(student=student, internship=internship)
        messages.success(request, 'Application submitted successfully!')
        return redirect('student_dashboard')
    
    return render(request, 'portal/internship_detail.html', {
        'internship': internship,
        'has_applied': has_applied
    })

@login_required
@user_passes_test(is_employer)
def application_list(request, internship_id):
    internship = get_object_or_404(Internship, internship_id=internship_id)
    company = Company.objects.get(employer=request.user)
    
    #verify that the internship belongs to the employer
    if internship.employer != company:
        messages.error(request, 'You do not have permission to view these applications.')
        return redirect('employer_dashboard')
    
    applications = Application.objects.filter(internship=internship)
    
    return render(request, 'portal/application_list.html', {
        'internship': internship,
        'applications': applications
    })

@login_required
@user_passes_test(is_employer)
def select_student(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    company = Company.objects.get(employer=request.user)
    
    # verify that the internship belongs to the employer
    if application.internship.employer != company:
        messages.error(request, 'You do not have permission to select students for this internship.')
        return redirect('employer_dashboard')
    
    if request.method == 'POST':
        # create offer
        offer_letter = request.FILES.get('offer_letter')
        if offer_letter:
            Offer.objects.create(application=application, offer_letter=offer_letter)
            
            # nark internship as pending
            internship = application.internship
            internship.status = 'pending'
            internship.save()
            
            # check co-op eligibility
            eligibility = check_coop_eligibility(application)
            
            if eligibility['is_eligible']:
                # send email to student
                send_mail(
                    'Co-op Eligibility Notification',
                    f'Congratulations! You have been selected for the internship and are eligible for co-op credit. Please log in to the portal to opt-in.',
                    settings.DEFAULT_FROM_EMAIL,
                    [application.student.email],
                    fail_silently=False,
                )
                messages.success(request, 'Student selected and notified about co-op eligibility!')
            else:
                messages.success(request, 'Student selected but not eligible for co-op.')
            
            return redirect('employer_dashboard')
        else:
            messages.error(request, 'Please upload an offer letter.')
    
    return render(request, 'portal/select_student.html', {'application': application})

@login_required
@user_passes_test(is_student)
def co_op_opt_in(request, application_id):
    from django.utils import timezone
    application = get_object_or_404(Application, id=application_id)
    student = Student.objects.get(user=request.user)
    
    # verify that the application belongs to the student
    if application.student != student:
        messages.error(request, 'You do not have permission to access this application.')
        return redirect('student_dashboard')
    
    # check if already opted in
    try:
        coop_registration = CoopRegistration.objects.get(application=application)
        form = CoopRegistrationForm(request.POST or None, instance=coop_registration)
    except CoopRegistration.DoesNotExist:
        form = CoopRegistrationForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        coop_registration = form.save(commit=False)
        coop_registration.application = application
        if coop_registration.opted_in:
            coop_registration.opted_in_at = timezone.now()
        coop_registration.save()
        messages.success(request, 'Co-op preference saved successfully!')
        return redirect('student_dashboard')
    
    # check eligibility
    eligibility = check_coop_eligibility(application)
    
    return render(request, 'portal/co_op_opt_in.html', {
        'form': form,
        'application': application,
        'eligibility': eligibility
    })

@login_required
@user_passes_test(is_student)
def submit_coop_summary(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    student = Student.objects.get(user=request.user)
    
    # verify that the application belongs to the student
    if application.student != student:
        messages.error(request, 'You do not have permission to access this application.')
        return redirect('student_dashboard')
    
    # check if summary already submitted
    try:
        coop_summary = CoopSummary.objects.get(application=application)
        form = CoopSummaryForm(request.POST or None, instance=coop_summary)
    except CoopSummary.DoesNotExist:
        form = CoopSummaryForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        coop_summary = form.save(commit=False)
        coop_summary.application = application
        coop_summary.save()
        messages.success(request, 'Co-op summary submitted successfully!')
        return redirect('student_dashboard')
    
    return render(request, 'portal/co_op_summary.html', {
        'form': form,
        'application': application
    })

@login_required
@user_passes_test(is_faculty)
def grade_student(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    faculty = Faculty.objects.get(user=request.user)
    
    # verify that the student is in the same department as the faculty
    if application.student.department != faculty.department:
        messages.error(request, 'You can only grade students from your department.')
        return redirect('faculty_dashboard')
    
    # check if grade already exists
    try:
        grade = Grade.objects.get(application=application)
        form = GradeForm(request.POST or None, instance=grade)
    except Grade.DoesNotExist:
        form = GradeForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        grade = form.save(commit=False)
        grade.application = application
        grade.entered_by = faculty
        grade.save()
        messages.success(request, 'Grade submitted successfully!')
        return redirect('faculty_dashboard')
    
    return render(request, 'portal/grade_student.html', {
        'form': form,
        'application': application
    })


@login_required
@user_passes_test(is_employer)
def edit_internship(request, internship_id):
    company = get_object_or_404(Company, employer=request.user)
    internship = get_object_or_404(Internship, internship_id=internship_id, employer=company)

    if internship.status == 'closed':
        messages.error(request, 'You cannot edit a closed internship.')
        return redirect('employer_dashboard')

    if internship.status == 'pending':
        messages.error(request, 'You cannot edit this posting because a student has already been selected.')
        return redirect('employer_dashboard')

    if request.method == 'POST':
        if 'close' in request.POST:
            internship.status = 'closed'
            internship.save(update_fields=['status'])
            messages.success(request, f'"{internship.title}" marked as Closed.')
            return redirect('employer_dashboard')

        form = InternshipForm(request.POST, instance=internship)
        if form.is_valid():
            form.save()
            messages.success(request, 'Internship updated.')
            return redirect('employer_dashboard')

    else:
        form = InternshipForm(instance=internship)

    return render(request, 'portal/edit_internship.html', {'form': form, 'internship': internship})
