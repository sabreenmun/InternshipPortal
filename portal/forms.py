from django import forms
from .models import Company, Student, Faculty, Internship, Application, CoopRegistration, CoopSummary, Grade

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['employer', 'employer_unique_id']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company location'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'contact_person_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact person name'
            }),
            'contact_person_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contact@example.com'
            }),
            'contact_person_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(123) 456-7890'
            }),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user', 'student_id']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(123) 456-7890'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'major': forms.Select(attrs={
                'class': 'form-select'
            }),
            'credit_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '1'
            }),
            'gpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.0',
                'max': '4.0',
                'step': '0.01'
            }),
            'start_semester': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fall 2023'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'is_transfer': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        exclude = ['user']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'faculty.email@example.com'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        exclude = ['employer', 'internship_id', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter internship title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the internship position, responsibilities, and requirements',
                'rows': 5
            }),
            'weeks': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'step': '1'
            }),
            'hours_per_week': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'step': '1'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter location or "Remote"'
            }),
            'majors': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Computer Science, Engineering, Business, etc.'
            }),
            'required_skills': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'List required skills separated by commas',
                'rows': 3
            }),
            'preferred_skills': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'List preferred skills separated by commas (optional)',
                'rows': 3
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter salary amount (optional)',
                'step': '0.01'
            }),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = []
        # No fields to style since it's empty

class CoopRegistrationForm(forms.ModelForm):
    class Meta:
        model = CoopRegistration
        fields = ['opted_in']
        widgets = {
            'opted_in': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['opted_in'].label = "I would like to receive co-op credit for this internship"

class CoopSummaryForm(forms.ModelForm):
    class Meta:
        model = CoopSummary
        fields = ['summary']
        widgets = {
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your internship experience, what you learned, and how it relates to your academic studies',
                'rows': 10
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['summary'].label = "Co-op Experience Summary"

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['grade']
        widgets = {
            'grade': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grade'].label = "Select Grade"

class InternshipSearchForm(forms.Form):
    title = forms.CharField(
        required=False, 
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by job title'
        })
    )
    location = forms.CharField(
        required=False, 
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by location'
        })
    )
    major = forms.CharField(
        required=False, 
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by major'
        })
    )