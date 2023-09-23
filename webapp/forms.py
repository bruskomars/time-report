from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from .models import User, DailyReport, TaskStatus

from django import forms
from django.forms.widgets import PasswordInput, TextInput
from django.forms import widgets


# Register
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'employee_id', 'first_name', 'last_name', 'password1', 'password2']


# Login
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# Add Daily Report
class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = '__all__'
        exclude = ['user', 'total_time']
        widgets = {
            'date': widgets.DateInput(attrs={'type': 'date'}),
            'time_start': widgets.TimeInput(attrs={'type': 'time'}),
            'time_end': widgets.TimeInput(attrs={'type': 'time'}),
        }

# Add Task Report
class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = TaskStatus
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'date_start': widgets.DateInput(attrs={'type': 'date'}),
            'date_finish': widgets.DateInput(attrs={'type': 'date'}),
        }