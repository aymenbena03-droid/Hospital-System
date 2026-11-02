from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Patient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class PatientRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=True, help_text="Enter your phone number.")
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
    
    def save(self, commit=True):
        # Save the user first
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Create the Patient profile and link it to this user
            Patient.objects.create(
                user= user,
                phone = self.cleaned_data['phone']
            )
        return user
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign Up', css_class='btn-primary w-100 rounded-pill mt-3'))
        
    
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input(Submit('submit', 'Login', css_class='btn-primary w-100 rounded-pill mt-3'))