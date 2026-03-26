from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Company(models.Model):
    employer = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    website = models.URLField()
    contact_person_name = models.CharField(max_length=100)
    contact_person_email = models.EmailField()
    contact_person_phone = models.CharField(max_length=15)
    employer_unique_id = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name

class Faculty(models.Model):
    DEPARTMENTS = (
        ('cs', 'Computer Science'),
        ('eng', 'Engineering'),
        ('bus', 'Business'),
        ('art', 'Arts'),
        ('sci', 'Science'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=3, choices=DEPARTMENTS)
    
    def __str__(self):
        return self.full_name

class Student(models.Model):
    DEPARTMENTS = (
        ('cs', 'Computer Science'),
        ('eng', 'Engineering'),
        ('bus', 'Business'),
        ('art', 'Arts'),
        ('sci', 'Science'),
    )
    
    MAJORS = (
        ('cs', 'Computer Science'),
        ('it', 'Information Technology'),
        ('ee', 'Electrical Engineering'),
        ('me', 'Mechanical Engineering'),
        ('ce', 'Civil Engineering'),
        ('bus', 'Business Administration'),
        ('acc', 'Accounting'),
        ('art', 'Art'),
        ('bio', 'Biology'),
        ('chem', 'Chemistry'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    department = models.CharField(max_length=3, choices=DEPARTMENTS)
    major = models.CharField(max_length=4, choices=MAJORS)
    credit_hours = models.PositiveIntegerField()
    gpa = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(4.0)])
    start_semester = models.CharField(max_length=10)  # e.g., "Fall 2023"
    is_transfer = models.BooleanField(default=False)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    student_id = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.full_name

class Internship(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('closed', 'Closed'),
    )
    
    employer = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    weeks = models.PositiveIntegerField()
    hours_per_week = models.PositiveIntegerField()
    location = models.CharField(max_length=200)
    majors = models.CharField(max_length=200)  # Comma-separated list of majors
    required_skills = models.TextField()
    preferred_skills = models.TextField(blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    internship_id = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.title

class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'internship']
    
    def __str__(self):
        return f"{self.student} - {self.internship}"

class Offer(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    offer_letter = models.FileField(upload_to='offer_letters/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Offer for {self.application.student}"

class CoopEligibility(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    is_eligible = models.BooleanField(default=False)
    reason = models.TextField(blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Eligibility for {self.application.student}: {self.is_eligible}"

class CoopRegistration(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    opted_in = models.BooleanField(default=False)
    opted_in_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Co-op registration for {self.application.student}"

class CoopSummary(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    summary = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Co-op summary for {self.application.student}"

class Grade(models.Model):
    GRADE_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    )
    
    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    entered_by = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    entered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Grade for {self.application.student}: {self.grade}"