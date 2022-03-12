from crispy_forms.bootstrap import StrictButton
from crispy_forms.layout import Layout
from django import forms
from .models import Student, Subject, CourseEnrollment, Settings

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserModel, User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'year']
        labels = {
            'full_name': 'Surname and first name',
            'year': 'Year'
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['course_name']
        labels = {
            'course_name': 'Course name',
        }


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = CourseEnrollment
        fields = ['student', 'subject']
        labels = {
            'student': 'Student',
            'subject': 'Course',
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = CourseEnrollment
        fields = ['grades']
        labels = {
            'grades': 'Grade'
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        cleaned_email = self.cleaned_data['email']

        try:
            if User.objects.get(email=cleaned_email) is not None:
                raise forms.ValidationError("There is already an account with the entered email!")
        except User.DoesNotExist:
            pass
        return cleaned_email


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = '__all__'
        labels = {
            'is_teacher': 'I am a teacher'
        }


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

        labels = {
            'email': 'Email'
        }
