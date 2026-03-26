from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

#register a user.
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPES)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user_profile = user.userprofile
            user_profile.user_type = self.cleaned_data['user_type']
            user_profile.save()
        return user