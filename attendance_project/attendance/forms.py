from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django.views.i18n import JavaScriptCatalog
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit



class DateInput(forms.DateInput):
    input_type = 'date'
    
    

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)  
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))
    remember_me = forms.BooleanField(required=False)

  
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields = ['image']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields=['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
        

class EmployeeForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    admin = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    address = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 10}))
    
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'dob': DateInput(),
        }
    

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['attendance_date']
        widgets = {
            'attendance_date': DateInput(attrs={'class': 'datepicker','required':False})
        }


class LeaveReportEmployeeForm(forms.ModelForm):
        
    class Meta:
        model = LeaveReportEmployee
        fields = ['from_leave_date', 'to_leave_date', 'leave_message', 'leave_status']
        widgets = {
            'from_leave_date': DateInput(attrs={'class': 'datepicker', 'required': False}),
            'to_leave_date': DateInput(attrs={'class': 'datepicker', 'required': False})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.labels_uppercase = True
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Apply Leave'))


